import gradio as gr
from skimage import io
import cv2
import numpy as np

class PointManager:
    def __init__(self):
        self.points_list = []

    def load_img(self, img):
        self.image = io.imread(img.name)
        self.update_output_img(self.points_list)
        return self.image

    def update_output_img(self, points_list):
        self.output_img = self.image.copy()
        for point in points_list:
            cv2.circle(self.output_img, point, 3, (255, 0, 0), -1)

    def add_point(self, evt: gr.SelectData):
        self.points_list.append((evt.index[0], evt.index[1]))
        self.update_output_img(self.points_list)
        return self.points_list, self.output_img
    
    def remove_last_point(self):
        if self.points_list:
            self.points_list.pop()  # Remove the last point
            self.update_output_img(self.points_list)
        return self.points_list, self.output_img

point_manager = PointManager()

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Row():
            with gr.Column():
                with gr.Row():
                    upl_button = gr.UploadButton(value="upload image")
                    load_button = gr.Button("load the image")
                inp_img = gr.Image(label="loaded img")
                with gr.Column():
                    display_cord = gr.Textbox()
                    remove_button=gr.Button("Remove points")
            out_img = gr.Image(label="output img")
            load_button.click(fn=point_manager.load_img, inputs=upl_button, outputs=inp_img)
            inp_img.select(fn=point_manager.add_point, outputs=[display_cord, inp_img])
            remove_button.click(fn=point_manager.remove_last_point, outputs=[display_cord, inp_img])

demo.launch()
