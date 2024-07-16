import wave,os,PIL,sys,re
import PIL.Image
import numpy as np

def wav_to_binary(wav_file_path):
    # Open the .wav file
    with wave.open(wav_file_path, 'rb') as wav_file:
        # Extract parameters
        params = wav_file.getparams()
        n_channels, sampwidth, framerate, n_frames, comptype, compname = params[:6]

        # Read the frames
        frames = wav_file.readframes(n_frames)

        # Convert frames to binary data
        binary_data = ''.join(f'{byte:08b}' for byte in frames)
        bits = list(binary_data)
        return bits

def extract_number(filename):
    match = re.search(r'(\d+)\.png$', filename)
    return int(match.group(1)) if match else float('inf')

def binary_to_image(bits:list):
    os.system("clear")
    for i in range(int((len(bits)/4194304)+1)):
        print(f"Generating image {i+1}...",end='\r')
        ci=0+(4194304*i)
        img = None
        img = PIL.Image.new("1",(2048,2048))
        pixels = img.load()
        for y in range(2048):
            for x in range(2048):
                try: cp = int(bits[ci])
                except: cp=0
                pixels[x,y]=cp
                ci+=1
        img.save(f"gen/{f.replace(".wav","")}-{i+1}.png")

def combine_all():
    final = PIL.Image.new("1",(2048,2048*int((len(bits)/4194304)+1)))
    ci=0
    usorted=[]
    csorted=[]
    for i in os.listdir("gen"): usorted.append(i)
    csorted = sorted(usorted,key=extract_number)
    
    os.system("clear")
    for i in csorted:
        print(f"Inserting image {i}...",end='\r')
        im = PIL.Image.open(f"gen/{i}")
        final.paste(im,(0,0+(2048*ci)))
        ci+=1
    print("Saving image...",end='\r')
    final.save(f"{f.replace(".wav","")}.png")
    print("Cleaning up...",end='\r')
    for image in os.listdir("gen"):
        os.remove(f"gen/{image}")
    


if len(sys.argv)==1:
    for image in os.listdir("gen"):
        os.remove(f"gen/{image}")

os.system("clear")
f = input("file (must be .wav): ")
print("Converting to binary...",end='\r')
bits = wav_to_binary(f)
print(f"pixels: {len(bits)}\nimage size: 2048x2048\nnumber of images: {int((len(bits)/4194304)+1)}",end='\r')
if len(sys.argv)>1:
    if sys.argv[1]=="-skip-gen":
        print("Combining...",end='\r')
        combine_all()
        exit()
else:
    print(f"creating images...",end='\r')
    binary_to_image(bits)
print("Combining...",end='\r')
combine_all()
print("Done.",end='\r')
