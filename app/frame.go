package main

import (
	"bytes"
	"fmt"
	"image"
	"image/jpeg"
	"net"
)

func Byte2Int(buf []byte) int {
	result := int(buf[0])*(256*256*256) + int(buf[1])*(256*256) + int(buf[2])*256 + int(buf[3])
	return result
}

func GetFrame(sock net.Conn) (image.Image, error) {
	var buf bytes.Buffer
	len_buf := make([]byte, 4)
	recved := 0

	_, e := sock.Read(len_buf)
	if e != nil {
		return nil, e
	}

	length := Byte2Int(len_buf)

	for {
		tmp := make([]byte, 1024)
		n, e := sock.Read(tmp)
		if e != nil {
			return nil, e
		}
		recved += n
		fmt.Println(recved)
		buf.Write(tmp)

		if recved >= length {
			break
		}
	}

	reader := bytes.NewReader(buf.Bytes())
	img, e := jpeg.Decode(reader)

	if e != nil {
		return nil, e
	}

	return img, nil
}
