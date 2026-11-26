// Box.asm
// For K = 27:
// Starts at Row 27 (SCREEN + 32*27 = 16384 + 864 = 17248)
// Height = 20 rows, Width = 16 * ((27 mod 4) + 1) = 64 pixels (4 words per row)

(CHECK_KEY)
    @KBD
    D=M
    @FILL_BOX
    D;JNE

(CLEAR_BOX)
    @fill_val
    M=0
    @SETUP
    0;JMP

(FILL_BOX)
    @fill_val
    M=-1

(SETUP)
    @SCREEN
    D=A
    @864
    D=D+A
    @screen_ptr
    M=D

    @20
    D=A
    @row_left
    M=D

(NEXT_ROW)
    @row_left
    D=M
    @CHECK_KEY
    D;JEQ

    @fill_val
    D=M
    @screen_ptr
    A=M
    M=D
    A=A+1
    M=D
    A=A+1
    M=D
    A=A+1
    M=D

    @32
    D=A
    @screen_ptr
    M=D+M

    @row_left
    M=M-1

    @NEXT_ROW
    0;JMP
