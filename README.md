# gimp-stable-diffusion (replicate.com fork)

This repository includes a GIMP plugin for communication with the  stable-diffusion model on replicate.com.

It is a fork of <https://github.com/blueturtleai> which provides plugins backed by a Colb notbook, or by <https://stablehorde.net/>. Hopefully at some point a single great plugin will just support many different backends.

Please check HISTORY.md for the latest changes.

## Installation
### Download files

To download the files of this repository click on "Code" and select "Download ZIP". In the ZIP you will find the file "gimp-stable-diffusion.py". This is the code for the GIMP plugin. You don't need the other files in the ZIP.

### GIMP

The plugin is tested in GIMP 2.10 and runs most likely in all 2.* releases. Excluded is 2.99, because it's already Python 3 based.

1. Start GIMP and open the preferences dialog via edit/preferences and scroll down to "folders". Expand "folders" and click on "plug-ins". Select the folder which includes your username and copy the path.

2. Open the file explorer, navigate to this directory and copy the file "gimp-stable-diffusion.py" from the repository into this directory. If you are on MacOS or Linux, change the file permissions to 755.

3. Restart GIMP. You should now see the new menu "AI". If you don't see this, something went wrong. Please check in this case "Troubleshooting/GIMP" for possible solutions. The menu has one item "Replicate.com img2img". This item can't currently be selected. This only works, when you opened an image before.

## Generate images
Now we are ready for generating images.

1. Start GIMP and open an image or create a new one. It is recommended, that the image size is not larger than 512x512 as the model has been trained on this size. If you want to have larger images, use an external upscaler instead. The generated image will have the dimensions of the init image. But it may be resized to make sure, that the dimensions are a multiple of 64. The larger the image, the longer it takes to generate it and the more GPU ressources and RAM is used. If it is too larger, you will run out of memory.

2. Select the new AI/Stable im2img menu item. A dialog will open, where you can enter the details for the image generation.

   - **Use init image:** If you want to seed the process with the current image or start from scratch (like with text2img).

     TODO: Support proper inpainting with a mask.

   - **Prompt Strength:** Prompt strength when using init image. 1.0 corresponds to full destruction of information in init image. 0.8 is a good value to use.

   - **Guidance Scale:** Scale for classifier-free guidance. 7.5 is a good value to use.

   - **Steps:** How many steps the AI should use to generate the image. The higher the value, the more the AI will work on details. But it also means, the longer the generation takes and the more expensive the run is. 50 is a good value to use.

   - **Seed:** This parameter is optional. If it is empty, a random seed will be generated on the server. If you use a seed, the same image is generated again in the case the same parameters for init strength, steps, etc. are used. A slightly different image will be generated, if the parameters are modified.

     TODO: Include the seed somehow in the output (layer name?)

   - **Number of images:** Number of images, which are created in one run. The more images you create, the more server ressources will be used and the longer you have to wait until the generated images are displayed in GIMP.

   - **Prompt:** How the generated image should look like.

   - **Replicate.com token:** Insert the replicate.com token found on <https://replicate.com/account>. Do not share this with others (e.g. in screenshots)

3. Click on the OK button. The values you inserted into the dialog and the init image will be transmitted to the server, which starts now generating the image. When the image has been generated successfully, it will be shown as a new image in GIMP.

<!--

not done yet

### Inpainting 
Inpainting means replacing a part of an existing image. For example if you don't like the face on an image, you can replace it. **Inpainting is currently still in experimental stage. So, please don't expect perfect results.** The experimental stage is caused by the server side and not by GIMP.

For inpainting it's necessary to prepare the input image because the AI needs to know which part you want to replace. For this purpose you replace this image part by transparency. To do so, open the init image in GIMP and select "Layer/Transparency/Add alpha channel". Select now the part of the image which should be replaced and delete it. You can also use the eraser tool. 

For the prompt you use now a description of the new image. For example the image shows currently "a little girl running over a meadow with a balloon" and you want to replace the balloon by a parachute. You just write now "a little girl running over a meadow with a parachute".

-->

## Troubleshooting
### GIMP
#### AI menu is not shown
##### Linux
   - If you get this error ```gimp: LibGimpBase-WARNING: gimp: gimp_wire_read(): error```, it's very likely, that you have a GIMP version installed, which doesn't include Python. Check, if you have got the menu "Filters > Python-Fu > Console". If it is missing, please install GIMP from here: https://flathub.org/apps/details/org.gimp.GIMP.

##### macOS
   - Please double check, if the permissions of the plugin py file are set to 755. It seems, that changing permissions doesn't work via the file manager. Please open a terminal, cd to the plugins directory and run "chmod ugo+x *py".
   
##### macOS/Linux
   - Open a terminal an try to run the plugin py file manually via ```python <path-to-plugin-folder>/gimp-stable-diffusion.py```. You should see the error message, that "gimpfu" is unknown. Make sure, that you are running Python 2, as this version is used by GIMP. If other errors occur, please reinstall GIMP.

## FAQ

**Will GIMP 3 be supported?**
Yes, the plugin will be ported to GIMP 3.

**How do I report an error or request a new feature?** Please open a new issue in this repository.


