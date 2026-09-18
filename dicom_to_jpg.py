import pydicom
import numpy as np
from PIL import Image
import os
import argparse

def convert_dcm_to_jpg(dcm_path, jpg_path):
    """
    Converte um único arquivo DICOM para JPG.
    """
    try:
        # Lê o arquivo DICOM
        ds = pydicom.dcmread(dcm_path)
    except Exception as e:
        print(f"Erro ao ler {dcm_path}: {e}")
        return False
        
    try:
        # Obtém a matriz de pixels
        pixel_array = ds.pixel_array
        shape = pixel_array.shape
        
        is_rgb = False
        samples_per_pixel = getattr(ds, 'SamplesPerPixel', 1)
        if samples_per_pixel == 3:
            is_rgb = True
            
        # Lidando com múltiplos frames
        if len(shape) == 4: # Múltiplos frames RGB (frames, linhas, colunas, 3)
            print(f"Aviso: {dcm_path} contém múltiplos frames. Apenas o primeiro será convertido.")
            image_data = pixel_array[0]
        elif len(shape) == 3 and not is_rgb: # Múltiplos frames tons de cinza (frames, linhas, colunas)
            print(f"Aviso: {dcm_path} contém múltiplos frames. Apenas o primeiro será convertido.")
            image_data = pixel_array[0]
        else:
            image_data = pixel_array # (linhas, colunas) ou (linhas, colunas, 3)
            
        bits_allocated = getattr(ds, 'BitsAllocated', 8)
        
        # Só faz o rescale (ajuste de brilho/contraste) se for > 8 bits 
        # (geralmente exames médicos de 12/16 bits) ou tons de cinza.
        # Evitamos rescale em imagens RGB 8-bits para não distorcer as cores reais.
        if bits_allocated > 8 or (not is_rgb):
            image_data = image_data.astype(float)
            img_min = image_data.min()
            img_max = image_data.max()
            if img_max > img_min:
                image_data = ((image_data - img_min) / (img_max - img_min)) * 255.0
                
        # Converte para uint8 (inteiro de 8 bits)
        image_data = np.uint8(image_data)
        
        # Cria a imagem com o Pillow e salva como JPG
        # Nota: Imagens de ultrassom costumam vir do pydicom já em formato RGB real, 
        # mesmo que o cabeçalho diga YBR, por causa do descompressor interno.
        if is_rgb:
            img = Image.fromarray(image_data, 'RGB')
        else:
            img = Image.fromarray(image_data)
            
        img.save(jpg_path)
        
        print(f"Convertido: {dcm_path} -> {jpg_path}")
        return True
        
    except Exception as e:
        print(f"Erro ao processar os pixels de {dcm_path}: {e}")
        return False

def convert_folder(input_dir, output_dir):
    """
    Converte todos os arquivos .dcm de uma pasta.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.dcm'):
            dcm_path = os.path.join(input_dir, filename)
            jpg_filename = os.path.splitext(filename)[0] + '.jpg'
            jpg_path = os.path.join(output_dir, jpg_filename)
            convert_dcm_to_jpg(dcm_path, jpg_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # Modo terminal (como estava antes)
        parser = argparse.ArgumentParser(description='Conversor de imagens DICOM (.DCM) para JPG.')
        parser.add_argument('input', help='Caminho do arquivo DICOM de entrada ou pasta contendo arquivos DICOM.')
        parser.add_argument('output', help='Caminho do arquivo JPG de saída ou pasta de saída.')
        args = parser.parse_args()
        
        if os.path.isdir(args.input):
            convert_folder(args.input, args.output)
        elif os.path.isfile(args.input):
            if os.path.isdir(args.output):
                jpg_filename = os.path.splitext(os.path.basename(args.input))[0] + '.jpg'
                output_path = os.path.join(args.output, jpg_filename)
            else:
                output_path = args.output
            convert_dcm_to_jpg(args.input, output_path)
        else:
            print(f"Caminho de entrada não encontrado: {args.input}")
    else:
        # Modo "clique duplo" - abre janelas para escolher as pastas
        print("--- Conversor DICOM para JPG ---")
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw() # Esconde a janela base do tkinter
            
            print("1. Selecione a pasta que contém as imagens DICOM originais...")
            input_dir = filedialog.askdirectory(title="1. Selecione a pasta com imagens DICOM")
            
            if input_dir:
                print("2. Selecione a pasta onde deseja salvar os JPGs...")
                output_dir = filedialog.askdirectory(title="2. Selecione a pasta para salvar os JPGs")
                
                if output_dir:
                    print(f"\nIniciando conversão...")
                    print(f"De: {input_dir}")
                    print(f"Para: {output_dir}\n")
                    convert_folder(input_dir, output_dir)
                    print("\nConversão concluída!")
                else:
                    print("Operação cancelada: Pasta de destino não selecionada.")
            else:
                print("Operação cancelada: Pasta de origem não selecionada.")
                
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            
    print("\n==================================")
    input("Pressione Enter para fechar a tela...")
##desenvolvido por Luiz Weber e Guilherme P.