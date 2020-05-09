#include <libuvc/libuvc.h>

int main() {
    uvc_context_t *ctx;
    uvc_init(&ctx, nullptr);
    uvc_exit(ctx);
    return 0;
}
