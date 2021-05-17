package main

import (
	"fmt"
	"image/png"
	"os"
	"time"

	"golang.org/x/mobile/app"
	"golang.org/x/mobile/event/lifecycle"
	"golang.org/x/mobile/event/paint"
	"golang.org/x/mobile/event/touch"
	"golang.org/x/mobile/exp/sprite"
)

var eng sprite.Engine

func event_loop(a app.App) {
	for e := range a.Events() {
		switch e := a.Filter(e).(type) {
		case lifecycle.Event:
			if e.To.String() == "StageDead" {
				panic(0)
			}
		case paint.Event:
			fmt.Println("paint")
		case touch.Event:
			fmt.Println(e.X)
		}
	}
}

func subroutine() {
	for {
		f, e := os.Open("gopher.png")

		if e != nil {
			panic(e)
		}

		img, e := png.Decode(f)

		if e != nil {
			panic(e)
		}

		fmt.Println(img.At(300, 300))
		time.Sleep(time.Second * 1)
	}
}

func main() {
	go subroutine()
	app.Main(event_loop)
	fmt.Println("abc")
}
