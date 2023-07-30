from django.shortcuts import render,redirect
from django.contrib import messages
from .models import ImageFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import cv2
import os
from django.http import FileResponse
import mimetypes

def remove_old_files(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
            
def index(request,methods=["POST",'GET']):
    remove_old_files('static/processed')
    remove_old_files('static/upload')
    ImageFile.objects.all().delete()    
    if request.method=='POST':
        if len(request.FILES)!=0:
            img_file = request.FILES['in-image']
            image_obj = ImageFile(img=img_file)
            image_obj.save()
            return redirect('/home')
        else:
            ImageFile.objects.all().delete()
            return redirect('/') 
    return render(request,"index.html")

def home(request): 
    if ImageFile.objects.exists():
        last_object = ImageFile.objects.latest('created_at')
        objs_to_delete = ImageFile.objects.exclude(pk=last_object.pk).order_by('-created_at')
        objs_to_delete.delete()
        context={
        "type":True,
        'obj': last_object
        }  
        return render(request,"home.html",context)
    return redirect('/')

def crop(request):
    if ImageFile.objects.exists():
        last_object = ImageFile.objects.latest('created_at')
        context={
        'obj': last_object
        }
        return render(request,"crop.html",context)    
    return redirect('/')
def crop_reset(request,methods=["POST"]):
    if request.method=='POST':
        if 'crop-button' in request.POST: 
            width = int(request.POST.get('cwidth'))
            height = int(request.POST.get('cheight'))
            position_x = int(request.POST.get('position-x'))
            position_y =int(request.POST.get('position-y'))
            last_object = ImageFile.objects.latest('created_at')
            if last_object.processed_img :
                processed_img_path = last_object.processed_img.path
                proimg = cv2.imread(processed_img_path)
                x1, y1 = position_x, position_y
                x2, y2 = position_x + width, position_y + height
                processed_img = proimg[y1:y2,x1:x2]
            else:
                original_img_path = last_object.img.path
                img = cv2.imread(original_img_path)
                x1, y1 = position_x, position_y
                x2, y2 = position_x + width, position_y + height
                processed_img =img[y1:y2, x1:x2]       
            processed_img_path = os.path.join(settings.MEDIA_ROOT, 'processed', 'processed_image.png')
            cv2.imwrite(processed_img_path, processed_img)
            with open(processed_img_path, 'rb') as f:
                last_object.processed_img.save('processed_image.png', ContentFile(f.read()), save=True)
            return redirect('/crop')
        
        elif 'reset-button' in request.POST:
            last_object = ImageFile.objects.latest('created_at')
            if last_object.processed_img:
                original_img_path = last_object.img.path
                img = cv2.imread(original_img_path)
                processed_img_path = os.path.join(settings.MEDIA_ROOT, 'processed', 'processed_image.png') 
                cv2.imwrite(processed_img_path, img) 
                with open(processed_img_path, 'rb') as f:
                    last_object.processed_img.save('processed_image.png', ContentFile(f.read()), save=True)                  
            return redirect('/crop')
    return redirect("/crop")  
        
def flip(request):
    if ImageFile.objects.exists():
        last_object = ImageFile.objects.latest('created_at')
        context={
        'obj': last_object
        }
        return render(request,"flip.html",context)    
    return redirect('/')

def dimensions(request): 
    if ImageFile.objects.exists():
        last_object = ImageFile.objects.latest('created_at')
        context={
        'obj': last_object,
        "type":True,
        }
        return render(request,"home.html",context)    
    return redirect('/')

def percentage(request):
    if ImageFile.objects.exists():
        last_object = ImageFile.objects.latest('created_at')
        context={
        'obj': last_object,
        "type":False,
        }
        return render(request,"home.html",context)    
    return redirect('/')

def fliprotate(request,methods=['GET','POST']):
    if request.method == 'POST':
        if 'flip_horizontal' in request.POST:        
            last_object = ImageFile.objects.latest('created_at')
            if last_object.processed_img :
                processed_img_path = last_object.processed_img.path
                proimg = cv2.imread(processed_img_path)
                processed_img = cv2.flip(proimg, 1) 
            else:
                original_img_path = last_object.img.path
                img = cv2.imread(original_img_path)
                processed_img = cv2.flip(img, 1) 
                          
            processed_img_path = os.path.join(settings.MEDIA_ROOT, 'processed', 'processed_image.png')
            cv2.imwrite(processed_img_path, processed_img)
            with open(processed_img_path, 'rb') as f:
                last_object.processed_img.save('processed_image.png', ContentFile(f.read()), save=True)                
            redirect('/flip')
          
        elif 'flip_vertical' in request.POST:
            last_object = ImageFile.objects.latest('created_at')
            if last_object.processed_img :
                processed_img_path = last_object.processed_img.path
                proimg = cv2.imread(processed_img_path)
                processed_img = cv2.flip(proimg, 0) 
            else:
                original_img_path = last_object.img.path
                img = cv2.imread(original_img_path)
                processed_img = cv2.flip(img, 0) 
                          
            processed_img_path = os.path.join(settings.MEDIA_ROOT, 'processed', 'processed_image.png')
            cv2.imwrite(processed_img_path, processed_img)
            with open(processed_img_path, 'rb') as f:
                last_object.processed_img.save('processed_image.png', ContentFile(f.read()), save=True)
            redirect('/flip')  
    

        elif 'rotate_clockwise' in request.POST:
            last_object = ImageFile.objects.latest('created_at')
            if last_object.processed_img :
                processed_img_path = last_object.processed_img.path
                proimg = cv2.imread(processed_img_path)
                processed_img = cv2.rotate(proimg, cv2.ROTATE_90_CLOCKWISE) 
            else:
                original_img_path = last_object.img.path
                img = cv2.imread(original_img_path)
                processed_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE) 
                          
            processed_img_path = os.path.join(settings.MEDIA_ROOT, 'processed', 'processed_image.png')
            cv2.imwrite(processed_img_path, processed_img)
            with open(processed_img_path, 'rb') as f:
                last_object.processed_img.save('processed_image.png', ContentFile(f.read()), save=True)
            redirect('/flip')
        
        elif 'rotate_anticlockwise' in request.POST:
            last_object = ImageFile.objects.latest('created_at')
            if last_object.processed_img :
                processed_img_path = last_object.processed_img.path
                proimg = cv2.imread(processed_img_path)
                processed_img = cv2.rotate(proimg, cv2.ROTATE_90_COUNTERCLOCKWISE) 
            else:
                original_img_path = last_object.img.path
                img = cv2.imread(original_img_path)
                processed_img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE) 
                          
            processed_img_path = os.path.join(settings.MEDIA_ROOT, 'processed', 'processed_image.png')
            cv2.imwrite(processed_img_path, processed_img)
            with open(processed_img_path, 'rb') as f:
                last_object.processed_img.save('processed_image.png', ContentFile(f.read()), save=True)
            redirect('/flip')
            
    return redirect('/flip')
    
def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

def services(request):
    return render(request,"services.html")

def resize(request,mehods=["POST"]):
    if request.method == 'POST':
        Type = request.POST.get('type','')
        width = int(request.POST.get('width', 0))
        height = int(request.POST.get('height', 0))
        file_format = request.POST.get('format')
        print('file_format'+ file_format)
        size_percentage = int(request.POST.get('size-per', 0))
        unit = request.POST.get('unit', '')  # 'pixel', 'inch', 'cm', 'mm'
        last_object = ImageFile.objects.latest('created_at')
        original_extension = os.path.splitext(os.path.basename(last_object.img.name))[1]
        file_extension = original_extension if file_format == 'original' else '.' + file_format     
        new_processed_img_name = os.path.splitext(os.path.basename(last_object.img.name))[0] + '_new' + file_extension     
                  
        if last_object.processed_img:
            processed_img_path = last_object.processed_img.path
            proimg = cv2.imread(processed_img_path)
            conversion_factors = {
                'pixel': 1,
                'inch': 96,  # 1 inch = 96 pixels (assuming standard screen resolution)
                'cm': 37.8,  # 1 cm = 37.8 pixels (assuming standard screen resolution)
                'mm': 3.78,  # 1 mm = 3.78 pixels (assuming standard screen resolution)
            }

            if unit in conversion_factors:
                width_pixels = int(width * conversion_factors[unit])
                height_pixels = int(height * conversion_factors[unit])
            else:
                # If the unit is not recognized, default to pixels
                width_pixels = width
                height_pixels = height
            # Perform resizing based on the selected option
            if Type == 'dimensions':
                processed_img = cv2.resize(proimg, (width_pixels, height_pixels))
                processed_img_path =  os.path.join(settings.MEDIA_ROOT, 'processed', new_processed_img_name) 
                cv2.imwrite(processed_img_path, processed_img)
                # with open(processed_img_path, 'rb') as f:
                #     last_object.processed_img.save('processed_image.png', ContentFile(f.read()), save=True) 
                # new_processed_img_path = os.path.join(settings.MEDIA_ROOT, 'processed', new_processed_img_name)      
                content_type, _ = mimetypes.guess_type(processed_img_path)
                response = FileResponse(open(processed_img_path, 'rb'), content_type=content_type)
                response['Content-Disposition'] = f'attachment; filename="{new_processed_img_name}"'
                return response    
            elif Type == 'percentage':
                processed_img = cv2.resize(proimg, (0, 0), fx= size_percentage / 100, fy=size_percentage / 100)
                processed_img_path =  os.path.join(settings.MEDIA_ROOT, 'processed', new_processed_img_name) 
                cv2.imwrite(processed_img_path, processed_img)
                # with open(processed_img_path, 'rb') as f:
                #     last_object.processed_img.save('processed_image.png', ContentFile(f.read()), save=True) 
                # new_processed_img_path = os.path.join(settings.MEDIA_ROOT, 'processed', new_processed_img_name)      
                content_type, _ = mimetypes.guess_type(processed_img_path)
                response = FileResponse(open(processed_img_path, 'rb'), content_type=content_type)
                response['Content-Disposition'] = f'attachment; filename="{new_processed_img_name}"'
                return response    
        else:
            original_img_path = last_object.img.path
            img = cv2.imread(original_img_path)
            conversion_factors = {
                'pixel': 1,
                'inch': 96,  # 1 inch = 96 pixels (assuming standard screen resolution)
                'cm': 37.8,  # 1 cm = 37.8 pixels (assuming standard screen resolution)
                'mm': 3.78,  # 1 mm = 3.78 pixels (assuming standard screen resolution)
            }

            if unit in conversion_factors:
                width_pixels = int(width * conversion_factors[unit])
                height_pixels = int(height * conversion_factors[unit])
            else:
                # If the unit is not recognized, default to pixels
                width_pixels = width
                height_pixels = height
            # Perform resizing based on the selected option
            if Type == 'dimensions':
                processed_img = cv2.resize(img, (width_pixels, height_pixels))
                processed_img_path =  os.path.join(settings.MEDIA_ROOT, 'processed', new_processed_img_name) 
                cv2.imwrite(processed_img_path, processed_img)
                # with open(processed_img_path, 'rb') as f:
                #     last_object.processed_img.save('processed_image.png', ContentFile(f.read()), save=True) 
                # new_processed_img_path = os.path.join(settings.MEDIA_ROOT, 'processed', new_processed_img_name)      
                content_type, _ = mimetypes.guess_type(processed_img_path)
                response = FileResponse(open(processed_img_path, 'rb'), content_type=content_type)
                response['Content-Disposition'] = f'attachment; filename="{new_processed_img_name}"'
                return response      
            elif Type == 'percentage':
                processed_img = cv2.resize(img, (0, 0), fx= size_percentage / 100, fy=size_percentage / 100)
                processed_img_path =  os.path.join(settings.MEDIA_ROOT, 'processed', new_processed_img_name) 
                cv2.imwrite(processed_img_path, processed_img)
                # with open(processed_img_path, 'rb') as f:
                #     last_object.processed_img.save('processed_image.png', ContentFile(f.read()), save=True) 
                # new_processed_img_path = os.path.join(settings.MEDIA_ROOT, 'processed', new_processed_img_name)      
                content_type, _ = mimetypes.guess_type(processed_img_path)
                response = FileResponse(open(processed_img_path, 'rb'), content_type=content_type)
                response['Content-Disposition'] = f'attachment; filename="{new_processed_img_name}"'
                return response                    
        return redirect('/home')

    return render(request, '/')
        
def reset (request):
    processed_dir = os.path.join(settings.MEDIA_ROOT, 'processed')
    last_object = ImageFile.objects.latest('created_at')
    if last_object.processed_img:
            last_object.processed_img.delete()
            last_object.processed_img = None
            last_object.save()
    return redirect(request.META.get('HTTP_REFERER'))
    