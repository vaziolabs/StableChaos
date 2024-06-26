package main

import (
	"bytes"
	"compress/gzip"
	"fmt"
	"io/ioutil"
)

func compressString(input string) ([]byte, error) {
	var buf bytes.Buffer
	zw := gzip.NewWriter(&buf)

	_, err := zw.Write([]byte(input))
	if err != nil {
		return nil, err
	}

	if err := zw.Close(); err != nil {
		return nil, err
	}

	return buf.Bytes(), nil
}

func decompressString(compressed []byte) (string, error) {
	buf := bytes.NewBuffer(compressed)
	zr, err := gzip.NewReader(buf)
	if err != nil {
		return "", err
	}
	defer zr.Close()

	decompressed, err := ioutil.ReadAll(zr)
	if err != nil {
		return "", err
	}

	return string(decompressed), nil
}

func main() {
	input := "Hello, world! This is a test string to compress and decompress."
	fmt.Println("Original:", input)

	compressed, err := compressString(input)
	if err != nil {
		fmt.Println("Compression error:", err)
		return
	}

	fmt.Println("Compressed size:", len(compressed))

	decompressed, err := decompressString(compressed)
	if err != nil {
		fmt.Println("Decompression error:", err)
		return
	}

	fmt.Println("Decompressed:", decompressed)
}
