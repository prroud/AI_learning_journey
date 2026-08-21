from manim import *

class Data(Scene):
    def construct(self):


        w_tracker = ValueTracker(0.66)
        b_tracker = ValueTracker(0.27)

        raw_points = [(1.0, 3.4), (2.0, 5.1), (3.0, 6.3), (4.0, 8.2)]

        axes_data = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 10, 2],
            x_length=4.2,
            y_length=4.2,
            axis_config={"include_numbers": True}
        ).to_edge(LEFT, buff=0.6)

        title_data = Text("1. Przestrzeń danych", font_size=20, color=BLUE_B).next_to(axes_data, UP)

        dots_data = VGroup(*[
            Dot(axes_data.c2p(x, y), color=YELLOW, radius=0.08)
            for x, y in raw_points
        ])

        line = always_redraw(lambda: axes_data.plot(
            lambda x: w_tracker.get_value() * x + b_tracker.get_value(),
            color=BLUE,
            x_range=[0, 4.8]
        ))

        line_label = always_redraw(lambda: MathTex(
            f"y = {w_tracker.get_value():.2f}x + {b_tracker.get_value():.2f}",
            font_size=22,
            color=BLUE
        ).next_to(axes_data, DOWN, buff=0.2))

        axes_param = Axes(
            x_range=[0, 2.0, 0.5],
            y_range=[0, 3.0, 1.0],
            x_length=4.2,
            y_length=4.2,
            axis_config={"include_numbers": True}
        ).to_edge(RIGHT, buff=0.6)

        title_param = Text("2. Przestrzeń (w, b)", font_size=20, color=GREEN_B).next_to(axes_param, UP)
        axes_param_labels = axes_param.get_axis_labels(x_label="w", y_label="b")

        param_dot = always_redraw(lambda: Dot(
            axes_param.c2p(w_tracker.get_value(), b_tracker.get_value()),
            color=RED,
            radius=0.1
        ))

        target_center = axes_param.c2p(1.5, 2.0)
        contours = VGroup(*[
            Ellipse(width=i*0.7, height=i*1.2, color=DARK_GRAY, stroke_width=1.5).move_to(target_center)
            for i in range(1, 5)
        ])
        

        target_dot = Dot(target_center, color=GREEN, radius=0.06)
        target_label = MathTex("Min", font_size=16, color=GREEN).next_to(target_dot, UR, buff=0.05)

        self.play(
            Create(axes_data), Write(title_data), FadeIn(dots_data),
            Create(axes_param), Write(title_param), Write(axes_param_labels),
            Create(contours), FadeIn(target_dot), Write(target_label)
        )
        self.play(Create(line), Write(line_label), FadeIn(param_dot))
        self.wait(0.5)


        banner = Text("Krok 1: Forward Propagation (Liczę błąd)", font_size=20, color=YELLOW).to_corner(UP)
        self.play(Write(banner))

        # Dynamiczne linie błędu (residuali)
        def get_error_lines():
            lines = VGroup()
            w = w_tracker.get_value()
            b = b_tracker.get_value()
            for x_val, y_val in raw_points:
                y_hat = w * x_val + b
                p_start = axes_data.c2p(x_val, y_hat)
                p_end = axes_data.c2p(x_val, y_val)
                lines.add(DashedLine(p_start, p_end, color=RED, dash_length=0.06))
            return lines

        error_lines = always_redraw(get_error_lines)
        self.play(Create(error_lines), run_time=1)
        self.play(Indicate(param_dot, color=RED, scale_factor=1.4))
        self.wait(1)

        banner_back = Text("Krok 2: Backpropagation (Liczę gradienty dL/dw, dL/db)", font_size=20, color=RED).to_corner(UP)
        self.play(Transform(banner, banner_back))

        formula = MathTex(
            r"\nabla L = \begin{bmatrix} \frac{\partial L}{\partial w} \\ \frac{\partial L}{\partial b} \end{bmatrix}",
            font_size=24, color=RED
        ).next_to(param_dot, UR, buff=0.1)

        grad_arrow = Arrow(
            start=axes_param.c2p(0.66, 0.27),
            end=axes_param.c2p(1.1, 1.1),
            color=RED,
            buff=0,
            max_tip_length_to_length_ratio=0.2
        )

        self.play(Create(grad_arrow), Write(formula))
        self.wait(1.5)
        self.play(FadeOut(grad_arrow), FadeOut(formula))

        banner_gd = Text("Krok 3: Gradient Descent (Aktualizuję parametry z Learning Rate)", font_size=18, color=GREEN).to_corner(UP)
        self.play(Transform(banner, banner_gd))

        steps = [
            (0.95, 0.80), 
            (1.20, 1.30), 
            (1.40, 1.70), 
            (1.50, 2.00)  
        ]

        for i, (next_w, next_b) in enumerate(steps, start=1):
            self.play(
                w_tracker.animate.set_value(next_w),
                b_tracker.animate.set_value(next_b),
                run_time=1.2,
                rate_func=smooth
            )
            self.wait(0.3)


        banner_final = Text("Model wyuczony! Błąd zminimalizowany.", font_size=20, color=BLUE).to_corner(UP)
        self.play(Transform(banner, banner_final))
        self.play(Indicate(line, color=GREEN), Indicate(param_dot, color=GREEN))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])