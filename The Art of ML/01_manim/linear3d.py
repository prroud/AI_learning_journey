from manim import *

class Linear3D(ThreeDScene):
    def construct(self):

        self.camera.background_color = "#020b1a"

        # -------------------------------------------------------------
        # Scene 4 - Linear function in 3D (Plane)
        # -------------------------------------------------------------

        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        title_text = Text("3-Dimensional Case", font_size=32, weight=BOLD, color="#fffcd6")
        title_box = SurroundingRectangle(title_text, buff=0.15, corner_radius=0.1, color="#78716c")
        title_group = VGroup(title_text, title_box).to_edge(UP, buff=0.3)

        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-4, 4, 1],
            x_length=4.5,
            y_length=4.5,
            z_length=4.5,
            axis_config={"include_numbers": False, "color": "#d3e7fa"}
        ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.5)


        x1_label = MathTex("x_1", color="#d3e7fa").next_to(axes.x_axis.get_end(), RIGHT, buff=0.15)
        x2_label = MathTex("x_2", color="#d3e7fa").next_to(axes.y_axis.get_end(), UP, buff=0.15)
        y_label = MathTex("y", color="#d3e7fa").next_to(axes.z_axis.get_end(), OUT, buff=0.15)
        axes_labels = VGroup(x1_label, x2_label, y_label)


        w1_tracker = ValueTracker(0.5)
        w2_tracker = ValueTracker(0.2)
        b_tracker = ValueTracker(0.0)


        def get_surface():
            w1 = w1_tracker.get_value()
            w2 = w2_tracker.get_value()
            b = b_tracker.get_value()
            
            return Surface(
                lambda u, v: axes.c2p(u, v, w1 * u + w2 * v + b),
                u_range=[-2.5, 2.5],
                v_range=[-2.5, 2.5],
                resolution=(12, 12),
                fill_opacity=0.6,
                checkerboard_colors=[BLUE_D, BLUE_E],
                stroke_width=0.5,
                stroke_color=WHITE
            )

        graph = always_redraw(get_surface)


        general_formula = MathTex("y = ", "w_1", "x_1 + ", "w_2", "x_2 + ", "b", font_size=36, color="#d3e7fa")
        general_formula.set_color_by_tex("w_1", YELLOW)
        general_formula.set_color_by_tex("w_2", RED)
        general_formula.set_color_by_tex("b", GREEN)

        dynamic_formula = always_redraw(
            lambda: MathTex(
                f"y = {w1_tracker.get_value():.1f}x_1 {w2_tracker.get_value():+.1f}x_2 {b_tracker.get_value():+.1f}",
                font_size=32,
                color="#d3e7fa"
            )
            .next_to(general_formula, DOWN, buff=0.3)
            .align_to(general_formula, LEFT)
        )

        weight1_info = MathTex(r"\mathbf{w_1}", r"\text{ --- weight for } x_1", font_size=26)
        weight1_info.set_color_by_tex(r"\mathbf{w_1}", YELLOW)

        weight2_info = MathTex(r"\mathbf{w_2}", r"\text{ --- weight for } x_2", font_size=26)
        weight2_info.set_color_by_tex(r"\mathbf{w_2}", RED)

        bias_info = MathTex(r"\mathbf{b}", r"\text{ --- bias (intercept)}", font_size=26)
        bias_info.set_color_by_tex(r"\mathbf{b}", GREEN)

        right_panel = VGroup(
            general_formula,
            dynamic_formula,
            weight1_info,
            weight2_info,
            bias_info
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        right_panel.to_edge(RIGHT, buff=0.8).shift(DOWN * 0.2)
        panel_box = SurroundingRectangle(right_panel, color="#78716c", buff=0.25, corner_radius=0.1)
        ui_panel_group = VGroup(right_panel, panel_box)


        self.add_fixed_in_frame_mobjects(title_text, title_box)
        self.play(Write(title_text))
        self.play(Create(title_box), run_time=1.2)
        

        self.play(FadeIn(axes), FadeIn(axes_labels))
        

        self.add_fixed_in_frame_mobjects(panel_box, right_panel)
        self.play(
            Create(panel_box),
            Write(general_formula),
            Write(dynamic_formula),
            Write(weight1_info),
            Write(weight2_info),
            Write(bias_info)
        )
        

        self.play(Create(graph))
        self.wait(1)


        self.play(w1_tracker.animate.set_value(0.7), run_time=1.5)
        self.wait(0.3)
        self.play(w1_tracker.animate.set_value(-0.5), run_time=1.5)
        self.wait(0.3)
        self.play(w1_tracker.animate.set_value(0.3), run_time=1)

        self.play(w2_tracker.animate.set_value(0.6), run_time=1.5)
        self.wait(0.3)
        self.play(w2_tracker.animate.set_value(-0.4), run_time=1.5)
        self.wait(0.3)
        self.play(w2_tracker.animate.set_value(0.3), run_time=1)

        self.play(b_tracker.animate.set_value(1.8), run_time=1.5)
        self.wait(0.3)
        self.play(b_tracker.animate.set_value(-1.2), run_time=1.5)
        self.wait(0.3)
        self.play(b_tracker.animate.set_value(0.0), run_time=1)


        self.play(
            w1_tracker.animate.set_value(0.5),
            w2_tracker.animate.set_value(-0.3),
            b_tracker.animate.set_value(1.0),
            run_time=2
        )
        self.wait(2)

        self.play(
            FadeOut(title_group),
            FadeOut(ui_panel_group),
            FadeOut(axes),
            FadeOut(axes_labels),
            FadeOut(graph)
        )


        # -------------------------------------------------------------
        # Scene 5 - Generalisation for n-dimension
        # -------------------------------------------------------------

        # Reset camera angle to 2D view for text layout
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        # 1. Title matching theme
        n_title_text = Text("Generalisation for n-dimensions", font_size=32, weight=BOLD, color="#fffcd6")
        n_title_box = SurroundingRectangle(n_title_text, buff=0.15, corner_radius=0.1, color="#78716c")
        n_title_group = VGroup(n_title_text, n_title_box).to_edge(UP, buff=0.3)

        self.add_fixed_in_frame_mobjects(n_title_group)
        self.play(Write(n_title_text), Create(n_title_box), run_time=1.2)
        self.wait(0.5)

        # 2. General scalar equation for n dimensions
        n_formula = MathTex(
            "y", "=", "w_1", "x_1", "+", "w_2", "x_2", "+", r"\dots", "+", "w_n", "x_n", "+", "b",
            font_size=34, color="#d3e7fa"
        ).move_to(UP * 2.0)

        n_formula.set_color_by_tex("w_1", YELLOW)
        n_formula.set_color_by_tex("w_2", YELLOW)
        n_formula.set_color_by_tex("w_n", YELLOW)
        n_formula.set_color_by_tex("b", GREEN)

        self.add_fixed_in_frame_mobjects(n_formula)
        self.play(Write(n_formula), run_time=1.5)
        self.wait(0.8)

        # 3. Vector definitions (W vector of weights, X vector of features)
        vec_W = MathTex(
            r"\mathbf{W} = \begin{bmatrix} w_1 \\ w_2 \\ \vdots \\ w_n \end{bmatrix}",
            font_size=32, color="#d3e7fa"
        )
        vec_W.set_color_by_tex("w_1", YELLOW)
        vec_W.set_color_by_tex("w_2", YELLOW)
        vec_W.set_color_by_tex("w_n", YELLOW)

        label_W = Text("Weight Vector", font_size=20, color=YELLOW).next_to(vec_W, DOWN, buff=0.2)
        group_W = VGroup(vec_W, label_W).move_to(LEFT * 3.2 + UP * 0.1)

        vec_X = MathTex(
            r"\mathbf{X} = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix}",
            font_size=32, color="#d3e7fa"
        )
        label_X = Text("Feature Vector", font_size=20, color="#d3e7fa").next_to(vec_X, DOWN, buff=0.2)
        group_X = VGroup(vec_X, label_X).move_to(RIGHT * 3.2 + UP * 0.1)

        self.add_fixed_in_frame_mobjects(group_W, group_X)
        self.play(
            Write(group_W),
            Write(group_X),
            run_time=2.0
        )
        self.wait(1.0)

        # 4. Transposition step (showing W^T)
        vec_WT = MathTex(
            r"\mathbf{W}^T = \begin{bmatrix} w_1 & w_2 & \dots & w_n \end{bmatrix}",
            font_size=32, color="#d3e7fa"
        ).move_to(DOWN * 1.0)
        vec_WT.set_color_by_tex("w_1", YELLOW)
        vec_WT.set_color_by_tex("w_2", YELLOW)
        vec_WT.set_color_by_tex("w_n", YELLOW)

        label_WT = Text("Transposed Weight Vector", font_size=18, color="#78716c").next_to(vec_WT, DOWN, buff=0.15)
        group_WT = VGroup(vec_WT, label_WT)

        self.add_fixed_in_frame_mobjects(group_WT)
        self.play(ReplacementTransform(group_W.copy(), group_WT), run_time=1.5)
        self.wait(1.0)

        # 5. Combining into vector product W^T X + b
        dot_product = MathTex(
            r"\mathbf{W}^T \mathbf{X} = w_1 x_1 + w_2 x_2 + \dots + w_n x_n",
            font_size=32, color="#d3e7fa"
        ).move_to(DOWN * 1.9)
        dot_product.set_color_by_tex("w_1", YELLOW)
        dot_product.set_color_by_tex("w_2", YELLOW)
        dot_product.set_color_by_tex("w_n", YELLOW)

        self.add_fixed_in_frame_mobjects(dot_product)
        self.play(Write(dot_product), run_time=1.5)
        self.wait(1.0)

        # 6. Final highlight box with vector form y = W^T X + b
        final_eq = MathTex(
            r"y = \mathbf{W}^T \mathbf{X} + b",
            font_size=42, color="#fffcd6"
        )
        final_eq.set_color_by_tex(r"\mathbf{W}", YELLOW)
        final_eq.set_color_by_tex("b", GREEN)

        final_box = SurroundingRectangle(final_eq, color=YELLOW, buff=0.25, corner_radius=0.1)
        final_group = VGroup(final_eq, final_box).move_to(DOWN * 2.9)

        self.add_fixed_in_frame_mobjects(final_group)
        self.play(
            FadeIn(final_group, shift=UP * 0.2),
            run_time=1.5
        )
        self.wait(3.0)

        self.play(FadeOut(n_title_text, n_title_box, n_formula, group_X, group_W, group_WT, dot_product, final_group))

