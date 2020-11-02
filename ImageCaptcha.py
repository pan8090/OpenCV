from captcha.image import ImageCaptcha

img=ImageCaptcha()
image=img.generate_image('python')
image.show()
#image.save('python.jpg')