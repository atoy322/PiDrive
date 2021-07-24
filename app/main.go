package main

import (
	"fmt"
	"image/color"

	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
)

func main() {
	myapp := app.New()
	myapp.Settings().SetTheme(theme.DarkTheme())
	mywin := myapp.NewWindow("PiDrive")

	text := canvas.NewText("Hello", color.White)
	s := widget.NewSlider(0, 10)
	s.Step = 0.001
	s.OnChanged = func(f float64) {
		fmt.Println(f)
	}

	spacer := layout.NewSpacer()

	content := container.NewVBox(
		spacer,
		text,
		spacer,
		s,
	)
	mywin.SetContent(content)

	mywin.ShowAndRun()
}
