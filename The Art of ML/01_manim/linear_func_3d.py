from manim import *

class Linear3D(ThreeDScene):
        def construct(self):
            title_text = Text("3-Dimensional Case", font_size=32, weight=BOLD, color="#fffcd6")
            title_box = SurroundingRectangle(title_text, buff=0.15, corner_radius=0.1, color="#78716c")
            title_group = VGroup(title_text, title_box).to_edge(UP, buff=0.3)
            
            self.add_fixed_in_frame_mobjects(title_group)

            axes = ThreeDAxes(
                x_range=[-3, 3, 1],
                y_range=[-3, 3, 1],
                z_range=[-3, 3, 1],
                x_length=4.5,
                y_length=4.5,
                z_length=4.5,
                axis_config={"color": "#d3e7fa"},
            ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)

            labels = axes.get_axis_labels(
                MathTex("x_1", color="#d3e7fa"),
                MathTex("x_2", color="#d3e7fa"),
                MathTex("y", color="#d3e7fa")
            )

            w1_tracker = ValueTracker(1.0)
            w2_tracker = ValueTracker(0.5)
            b_tracker = ValueTracker(0.0)

            def get_plane():
                w1 = w1_tracker.get_value()
                w2 = w2_tracker.get_value()
                b = b_tracker.get_value()
                
                plane = Surface(
                    lambda u, v: axes.c2p(u, v, w1 * u + w2 * v + b),
                    u_range=[-2, 2],
                    v_range=[-2, 2],
                    resolution=(15, 15),
                    fill_opacity=0.6,
                    fill_color=BLUE,
                    stroke_color=BLUE_A,
                    stroke_width=1,
                )
                return plane

            surface = always_redraw(get_plane)

            general_formula = MathTex("y = ", "w_1", " x_1 + ", "w_2", " x_2 + ", "b", font_size=36, color="#d3e7fa")
            general_formula.set_color_by_tex("w_1", YELLOW)
            general_formula.set_color_by_tex("w_2", GREEN)
            general_formula.set_color_by_tex("b", RED)

            formula_anchor = Dot(fill_opacity=0).next_to(general_formula, DOWN, buff=0.4).align_to(general_formula, LEFT)

            dynamic_formula = always_redraw(
                lambda: MathTex(
                    f"y = {w1_tracker.get_value():+.1f}x_1 {w2_tracker.get_value():+.1f}x_2 {b_tracker.get_value():+.1f}",
                    font_size=30,
                    color="#d3e7fa"
                ).move_to(formula_anchor.get_center(), aligned_edge=LEFT)
            )

            w1_info = MathTex(r"\mathbf{w_1}", r"\text{ --- weight 1}", font_size=24).set_color_by_tex(r"\mathbf{w_1}", YELLOW)
            w2_info = MathTex(r"\mathbf{w_2}", r"\text{ --- weight 2}", font_size=24).set_color_by_tex(r"\mathbf{w_2}", GREEN)
            bias_info = MathTex(r"\mathbf{b}", r"\text{ --- bias}", font_size=24).set_color_by_tex(r"\mathbf{b}", RED)

            right_panel = VGroup(
                general_formula,
                formula_anchor,
                dynamic_formula,
                Line(LEFT, RIGHT, color=GRAY_D, stroke_width=1.5).scale(1.2),
                w1_info,
                w2_info,
                bias_info
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

            right_panel.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.2)
            panel_box = SurroundingRectangle(right_panel, color="#78716c", buff=0.2, corner_radius=0.1)

            hud_group = VGroup(panel_box, right_panel)
            self.add_fixed_in_frame_mobjects(hud_group)

            self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

            self.play(Write(title_text))
            self.play(Create(title_box), run_time=1.0)
            
            self.play(
                FadeIn(axes),
                Write(labels),
                Create(panel_box),
                Write(general_formula),
                Write(dynamic_formula),
                Write(w1_info),
                Write(w2_info),
                Write(bias_info)
            )
            
            self.play(Create(surface))
            self.wait(1)

            self.begin_ambient_camera_rotation(rate=0.15)

            self.play(w1_tracker.animate.set_value(-1.5), run_time=2)
            self.wait(0.5)

            self.play(w2_tracker.animate.set_value(1.8), run_time=2)
            self.wait(0.5)

            self.play(b_tracker.animate.set_value(1.5), run_time=2)
            self.wait(0.5)
            self.play(b_tracker.animate.set_value(-1.5), run_time=2)
            self.wait(0.5)

            self.play(
                w1_tracker.animate.set_value(0.5),
                w2_tracker.animate.set_value(0.5),
                b_tracker.animate.set_value(0.0),
                run_time=2
            )
            self.wait(2)

            self.play(FadeOut(axes, labels, panel_box, general_formula, dynamic_formula, w1_info, w2_info, bias_info))