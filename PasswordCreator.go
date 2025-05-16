package main

/*
#include <stdlib.h>
*/
import "C"

import (
    "crypto/rand"
    "math/big"
)

const (
	lowercase = "abcdefghijklmnopqrstuvwxyz"
	uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	digits    = "0123456789"
	special    = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
)

//export CreatePassword
func CreatePassword() *C.char {
    const length = 16
    chars := lowercase + uppercase + digits + special
    buf := make([]byte, length)
    for i := range buf {
        idx, err := rand.Int(rand.Reader, big.NewInt(int64(len(chars))))
        if err != nil {
            // on error, return empty string
            return C.CString("")
        }
        buf[i] = chars[idx.Int64()]
    }
    return C.CString(string(buf))
}

func main() {}