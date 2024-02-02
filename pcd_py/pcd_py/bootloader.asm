[ORG 0x7c00]  ; Set origin address to 0x7c00

section .text
    jmp short start

    db "AOS++", 0
    db "Disk Error!", 0
start:
    mov ax, 0x07c0
    add ax, 0x20
    mov ss, ax
    mov sp, 0x4000
    mov ax, 0x07c0
    mov ds, ax
    
    ; Load OS into memory
    mov bx, 0x8000
    mov dh, 0x00
    mov dl, 0x00
    mov cx, 0x0002
    mov ah, 0x02
    int 0x13 ; Disk read interrupt

    ; Jump to OS
    jmp 0x8000

    times 510-($-$$) db 0  ; Fill up the rest of the boot sector with zeros
    dw 0xaa55             ; Boot signature