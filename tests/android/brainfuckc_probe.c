/* Test-only native callable harness. No BF compiler, interpreter or app policy. */
#include <ctype.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

typedef struct { uint64_t status, ticks; } result;
typedef result (*policy)(const uint8_t *, uint64_t, uint8_t *, uint64_t,
                         uint8_t *, uint64_t, uint64_t, uint64_t *);

static int hex(const char *text, uint8_t *bytes, size_t capacity) {
    if (!strcmp(text, "-")) return 0;
    size_t size = strlen(text);
    if (size % 2 || size / 2 > capacity) return -1;
    for (size_t i = 0; i < size; i += 2) {
        if (!isxdigit((unsigned char)text[i]) || !isxdigit((unsigned char)text[i+1])) return -1;
        unsigned value;
        if (sscanf(text + i, "%2x", &value) != 1) return -1;
        bytes[i/2] = (uint8_t)value;
    }
    return (int)(size / 2);
}

int main(int argc, char **argv) {
    if (argc != 2) return 64;
    char name[64], previous[64] = "", input_hex[129], expected_hex[129], path[1024];
    void *image = MAP_FAILED;
    size_t mapped_size = 0;
    unsigned count = 0;
    int fields;
    while ((fields = scanf("%63s %128s %128s", name, input_hex, expected_hex)) == 3) {
        uint8_t input[64], expected[64], output[64] = {0}, tape[4096] = {0};
        int input_size = hex(input_hex, input, sizeof(input));
        int expected_size = hex(expected_hex, expected, sizeof(expected));
        if (input_size < 0 || expected_size < 0) return 65;
        for (size_t i = 0; name[i]; ++i)
            if (!isalnum((unsigned char)name[i]) && name[i] != '_') return 65;
        if (strcmp(previous, name)) {
            if (image != MAP_FAILED) munmap(image, mapped_size);
            if (snprintf(path, sizeof(path), "%s/%s.elf", argv[1], name) >= (int)sizeof(path)) return 65;
            int fd = open(path, O_RDONLY);
            struct stat st;
            uint8_t header[128];
            if (fd < 0 || fstat(fd, &st) || st.st_size < 196 || read(fd, header, 128) != 128) return 66;
            if (memcmp(header, "\177ELF\2\1\1", 7) || memcmp(header+120, "BFP1", 4)
                    || header[18] != 183 || header[19] || header[24] != 128) return 66;
            mapped_size = (size_t)st.st_size;
            image = mmap(NULL, mapped_size, PROT_READ | PROT_EXEC, MAP_PRIVATE, fd, 0);
            close(fd);
            if (image == MAP_FAILED) { perror("mmap"); return 67; }
            strcpy(previous, name);
        }
        uint64_t used = UINT64_MAX;
        result actual = ((policy)((uint8_t *)image + 128))(
            input, (uint64_t)input_size, output, sizeof(output), tape, sizeof(tape), 2000000, &used);
        if (actual.status || used != (uint64_t)expected_size || used > sizeof(output)
                || memcmp(output, expected, (size_t)used)) {
            fprintf(stderr, "FAIL %s vector=%u status=%llu used=%llu expected=%d\n", name, count,
                    (unsigned long long)actual.status, (unsigned long long)used, expected_size);
            return 68;
        }
        ++count;
    }
    if (image != MAP_FAILED) munmap(image, mapped_size);
    if (fields != EOF || !count) return 69;
    printf("PASS %u native/reference comparisons\n", count);
    return 0;
}
