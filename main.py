import customtkinter as ctk
from PIL import Image, ImageFont, ImageDraw
from customtkinter import filedialog

class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        
        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('blue')
        
        self.geometry('900x700')
        self.config(padx=10, pady=10)
        self.title("Image Watermarker App")
        self.resizable(width=False, height=False)
        
        # ------------------------------------------------------WATERMARK PERSONALIZATION FRAME--------------------------------------#
        self.personalization_frame = ctk.CTkFrame(master=self, corner_radius=10,)
        self.personalization_frame.grid(row=0, column=0, pady=(5,0), rowspan=2 )
        
        # ------------------CUSTOMISE WATERMARK FRAME TITLE------------------------#
        self.title = ctk.CTkLabel(master=self.personalization_frame, text="Customise Watermark", fg_color="gray30", font=('./fonts/MERRIWEATHER-REGULAR.TTF', 20), padx=10, pady=10, corner_radius=10)
        self.title.grid(row=0, column=0, sticky='w', pady=15, padx=15)
        
        # -----------------------THEME SECTION---------------------#
        self.theme = ctk.CTkLabel(master=self.personalization_frame, text='Theme:')
        self.theme.grid(row=1, column=0, sticky='n',pady=(5,0))
        self.theme_var = ctk.StringVar()
        self.theme_dropdown = ctk.CTkComboBox(master=self.personalization_frame, values=['light', 'dark'], variable=self.theme_var)
        self.theme_dropdown.set('light')
        self.theme_dropdown.grid(row=2, column=0, sticky='n')
        
        # --------------------------MODE----------------------------#
        self.mode_label =  ctk.CTkLabel(master=self.personalization_frame, text='Mode:')
        self.mode_label.grid(row=3, column=0, sticky='n', pady=(15,0))
        self.mode_var = ctk.StringVar()
        self.mode_dropdown = ctk.CTkComboBox(master=self.personalization_frame, values=['top-left', 'top-right', 'bottom-right', 'bottom-left', 'center', 'tiles'], variable=self.mode_var)
        self.mode_dropdown.grid(row=4, column=0, sticky='n')
        self.mode_dropdown.set('center')
        
        # ------------------TRANSPARENCY LEVEL---------------------#
        self.trans_label = ctk.CTkLabel(self.personalization_frame, text='Opacity:')
        self.trans_label.grid(row=5, column=0, pady=(15,0))
        self.slider_var = ctk.IntVar()
        self.trans_slider = ctk.CTkSlider(master=self.personalization_frame, from_=1, to=100, progress_color='blue', variable=self.slider_var)
        self.trans_slider.set(15)
        self.trans_slider.grid(row=6, column=0)
        self.trans_slider_var = ctk.CTkLabel(master=self.personalization_frame, textvariable=self.slider_var, fg_color='gray20', corner_radius=10)
        self.trans_slider_var.grid(row=7, column=0 ,pady=(0,5))
        
        # --------------------WATAERMARK TEXT--------------------#
        self.text_var=str(ctk.StringVar())
        self.text_entry = ctk.CTkEntry(master=self.personalization_frame ,placeholder_text='Input your watermark text here!', width=260)
        self.text_entry.grid(row=8, column=0, pady=(340, 10))
        
        
        # ----------------------SELECTED IMAGE FRAME--------------------#

        self.image_selection_frame = ctk.CTkFrame(master=self)
        self.image_selection_frame.grid(row=0, column=1, sticky='n', pady=5, padx=50)

        self.original_label = ctk.CTkLabel(master=self.image_selection_frame, text='Original Image')
        self.original_label.grid(row=0, column=0, sticky='w', padx=10, )

        # ---BLANK IMAGE FOR WHEN NO PICTURE HAS BEEN UPLOADED ----#
        self.image  = Image.new(mode="RGBA", size=(530, 200), color='gray')
        # -------DISPLAY IMAGE ON FRAME-------#
        self.selected_image = ctk.CTkImage(light_image=self.image, dark_image=self.image, size=(530, 200))
        self.image_label = ctk.CTkLabel(master=self.image_selection_frame, image=self.selected_image, text="Image Preview")
        self.image_label.grid(row=1, column=0, pady=(5,15), columnspan=2)



        # --------SELECTED IMAGE FRAME BUTTONS-------#
        self.image_path_var = ctk.StringVar(master=self.image_selection_frame)
        self.select_button = ctk.CTkButton(master=self.image_selection_frame, command=self.select_image, text='select',fg_color='#007BFF', hover_color='#0056b3', width=245, )
        self.select_button.grid(row=2, column=0, sticky='w', padx=10, pady=(0,10))

        self.cancel_button = ctk.CTkButton(master=self.image_selection_frame, command=self.cancel, text='cancel', fg_color="#ff6f61", hover_color='#e55a4f', width=245)
        self.cancel_button.grid(row=2, column=1,padx=10, pady=(0,10), sticky='e')

        self.done_button = ctk.CTkButton(master=self.image_selection_frame, text='Done', width=510,fg_color='#007BFF', hover_color='#0056b3',command= self.submit)
        self.done_button.grid(row=3, column=0, columnspan=2, pady=(0,10))


        # --------------------WATERMARKED IMAGE PREVIEW FRAME -----------------------------#
        self.preview_frame = ctk.CTkFrame(master=self, )
        self.preview_frame.grid(row=1, column=1, pady=0, sticky='n')
        self.preview_label = ctk.CTkLabel(master=self.preview_frame, text='Watermarked',)
        self.preview_label.grid(row=0, column=0, sticky='w', padx=10)

        # ---BLANK IMAGE FOR WHEN NO PICTURE HAS BEEN WATERMARKED ----#
        self.watermark_preview_image = Image.new(mode="RGBA", size=(3000, 2700), color='lightslategray')
        
        # -------DISPLAY IMAGE ON FRAME-------#
        selected_image = ctk.CTkImage(light_image=self.watermark_preview_image, dark_image=self.watermark_preview_image, size=(530, 270))
        self.watermark_image_label = ctk.CTkLabel(master=self.preview_frame, image=selected_image, text="Watermark Preview")
        self.watermark_image_label.grid(row=1, column=0, pady=(5,10), columnspan=2)


        self.save_button = ctk.CTkButton(master=self.preview_frame, width=520, text='save',fg_color='#007BFF', hover_color='#0056b3', command=self.save)
        self.save_button.grid(row=2, column=0, columnspan=2, pady=(0,8))
        self.image_path = ''
        self.result = None
    def submit(self):
        self.watermark_image(image=self.image_path, watermark=self.text_entry.get(), mode=self.mode_var.get(), theme=self.theme_var.get(), opacity=self.slider_var.get())
        
    
    def watermark_image(self, image, opacity, mode,theme, watermark=''):
        '''watermark text o image'''
        'Watermark Single Image with text'
        image = Image.open(image).convert('RGBA')
        image_width, image_height= image.size
        opacity = int(opacity/100 *255)
        dark =(0, 0, 0, opacity)
        light = (255, 255, 255, opacity)
        
        if str(theme) == 'dark':
            watermark_color = dark
        else:
            str(theme) == 'light'
            watermark_color = light
        
        
        watermark_canva = Image.new(mode="RGBA", size=image.size, color=(0, 0, 0, 0))# -----CREATE BLANK CANVAS FOR THE WATERMARK TEXT TO BE WRITTEN
        # chaneg color to 0, 0, 0, 300 to invoke masking
        # -------creating ImageFont object
        font_size = int(image_width *0.05)
        font = ImageFont.truetype(font='./fonts/MONTSERRAT-VARIABLE-FONT_WEIGHT.ttf', size=font_size)
        
        # -----creating context for drawing watermark
        draw = ImageDraw.Draw(watermark_canva)
        text_width, text_height = draw.textsize(text=watermark, font=font)
            
        # Calculate position for the text to be centered
        x = (image_width - text_width) / 2
        y = (image_height - text_height) / 2
        
        # -----------------------DETERMINE WATERMARK MODE --------------------#
        if mode == "center":
            draw.text(xy=(x, y), text=watermark, fill=watermark_color, font=font)
        elif mode == "top-right":
            draw.text((image_width-text_width-10, 10), text=watermark, fill=watermark_color, font=font)
        elif mode == 'top-left':
            draw.text((10, 10), text=watermark, fill=watermark_color, font=font)
        elif mode == 'bottom-right':
            draw.text((image_width-text_width-10, image_height-text_height-10), text=watermark, fill=watermark_color, font=font)
        elif mode == "bottom-left":
            draw.text((10, image_height-text_height-10), text=watermark, fill=watermark_color, font=font)
        elif mode == 'tiles':
            # ------CREATE NEW IMAGE FOR THE ROTATED WATERMARK TEXT --------#
            text_image = Image.new('RGBA', (text_width, text_height), (255, 255, 255, 0))
            text_draw = ImageDraw.Draw(text_image)
            text_draw.text((0, 0), watermark, fill=watermark_color, font=font)
            
            
            rotated_text_image = text_image.rotate(angle=30, expand=1)
            #--------- Get the size of the rotated text image
            rotated_width, rotated_height = rotated_text_image.size
            
            
            #--------- Tile the rotated text image over the entire canvas
            for x in range(0, image_width, int(rotated_width*1.5)):
                for y in range(0, image_height, int(rotated_height*1.5)):
                    watermark_canva.paste(rotated_text_image, (x, y), rotated_text_image)
        
        
        self.result = Image.alpha_composite(im1=image, im2=watermark_canva)
        self.result.show()
        
        # ----------DISPLAY WATERMARKED IMAE IN FRAME -----------#
        
        watermarked_preview = self.result 
        # watermarked_preview = watermarked_preview.resize(530, 270, Image.LANCZOS)
        new_watermarked = ctk.CTkImage(light_image=watermarked_preview, dark_image=watermarked_preview, size=(530, 200))
        self.watermark_image_label.configure(image=new_watermarked, text='')
        
        
        # text.delete(0, END) thsi si used to clear the entrywidget. the text is just an object o fthe entery widget
    def cancel(self):
        '''reset screen to default'''
        # -----------reset original image preview screen--------#
        self.image  = Image.new(mode="RGBA", size=(530, 200), color='gray')
        self.selected_image = ctk.CTkImage(light_image=self.image, dark_image=self.image, size=(530, 200))
        self.image_label.configure(image=self.selected_image, text='Imaeg Preview')
        
        # ---------reset watermarked image preview screen -------#
        selected_image = ctk.CTkImage(light_image=self.watermark_preview_image, dark_image=self.watermark_preview_image, size=(530, 270))
        self.watermark_image_label.configure(image=selected_image, text='Watermark Preview')
        
        
    
    def get_watermark_text(self):
        '''Return watermark text value (25 characters)'''
        if len(self.text_var) > 15:
            self.text_var = self.text_var[:15]
        return self.text_var
    
    def select_image(self):
        '''select imaeg to watermark'''
        filename = filedialog.askopenfilename(title="Select an image", 
                                            filetypes=[
                                                ('Image', ['*.blp', '*.bmp', '*.dib', '*.bufr', '*.cur', '*.pcx', '*.dcx', '*.dds', '*.ps', '*.eps', '*.fit', '*.fits', '*.fli', '*.flc', '*.ftc', '*.ftu', '*.gbr', '*.gif', '*.grib', '*.h5', '*.hdf', '*.png', '*.apng', '*.jp2', '*.j2k', '*.jpc', '*.jpf', '*.jpx', '*.j2c', '*.icns', '*.ico', '*.im', '*.iim', '*.jfif', '*.jpe', '*.jpg', '*.jpeg', '*.mpg', '*.mpeg', '*.tif', '*.tiff', '*.msp', '*.pcd', '*.pxr', '*.pbm', '*.pgm', '*.ppm', '*.pnm', '*.psd', '*.qoi', '*.bw', '*.rgb', '*.rgba', '*.sgi', '*.ras', '*.tga', '*.icb', '*.vda', '*.vst', '*.webp', '*.wmf', '*.emf', '*.xbm', '*.xpm'
                                                        ])
                                                ]
                                            )
        # --------------CHANGE PREVIEW IMAGE ON DISPLAY
        self.image_path = filename
        self.image = Image.open(filename).convert('RGBA')
        self.image = self.image.resize((530, 200), Image.LANCZOS)
        
        new_selected_image = ctk.CTkImage(light_image=self.image, dark_image=self.image, size=(530, 200))
        self.image_label.configure(image=new_selected_image, text='')
        self.selected_image = new_selected_image
        
    def save(self):
        '''save image file after watermark'''
        save_filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if self.result:
            self.result.save(save_filename)
        
            
if __name__ == "__main__":        
    app = App()
    app.mainloop()

