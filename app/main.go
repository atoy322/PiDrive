package main

import (
	"fmt"
	"image/color"
	"net"

	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
)

func main() {
	ctrl_conn, e := net.Dial("tcp", "192.168.106.132:8080")
	if e != nil {
		panic(e)
	}
	stream_conn, e := net.Dial("tcp", "192.168.106.132:8000")
	if e != nil {
		panic(e)
	}
	go func() {
		for {
			buf := make([]byte, 1024)
			stream_conn.Read(buf)
		}
	}()
	//defer ctrl_conn.Close()
	//defer stream_conn.Close()

	myapp := app.New()
	myapp.Settings().SetTheme(theme.DarkTheme())
	mywin := myapp.NewWindow("PiDrive")

	text := canvas.NewText("Hello", color.White)
	s := widget.NewSlider(0, 40)
	s.Step = 1
	s.Value = 20
	s.OnChanged = func(f float64) {
		cmd := fmt.Sprintf("STEER:%d", int(f-20))
		fmt.Println(cmd)
		ctrl_conn.Write([]byte(cmd))
	}

	spacer := layout.NewSpacer()

	content := container.NewVBox(
		spacer,
		text,
		spacer,
		s,
	)
	mywin.SetContent(content)

	fmt.Println("start")
	mywin.ShowAndRun()
	fmt.Println("end")
}
