from django.shortcuts import render,redirect
from django.contrib import messages
from .models import ImageFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import cv2
import os

def index(request,methods=["POST",'GET']):
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
            # return render(request, 'flip.html', {'obj': last_object}) 
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