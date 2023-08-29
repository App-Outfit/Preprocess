import cv2
from PIL import Image
import matplotlib.pyplot as plt
import subprocess
import os
import shutil
import sys


base = '/content/gdrive/MyDrive/'
process = 'background_removal_DL/'
test_data_path = os.path.join(base, process, 'test_data/images')

u2result_path = os.path.join(test_data_path, 'u2net_results/input.png')
input_path = os.path.join(test_data_path, 'input/input.jpg')
output_path = os.path.join(test_data_path, 'output/output.png')

def move_and_rename_file(src_path, dest_folder, new_name="input.jpg"):
    if not os.path.exists(src_path):
        print(f"Erreur : Le fichier source {src_path} n'existe pas.")
        return None
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    dest_path = os.path.join(dest_folder, new_name)
    
    try:
        shutil.move(src_path, dest_path)
        print(f"Le fichier a été déplacé et renommé en {dest_path}.")
        return dest_path
    except Exception as e:
        print(f"Erreur lors du déplacement ou du renommage du fichier : {e}")
        return None


def background_removal():
    # Changer de répertoire
    os.chdir(test_data_path)

    # Exécuter le script Python
    subprocess.run(['python', 'u2net_image.py'])

    # Traiter les images
    u2netresult = cv2.imread(u2result_path)
    original = cv2.imread(input_path)
    subimage = cv2.subtract(u2netresult, original)
    cv2.imwrite(output_path, subimage)

    # Ouvrir les images avec PIL
    subimage = Image.open(output_path)
    original = Image.open(input_path)

    # Convertir les images en RGBA
    subimage = subimage.convert("RGBA")
    original = original.convert("RGBA")

    # Obtenir les données des images
    subdata = subimage.getdata()
    ogdata = original.getdata()

    # Créer de nouvelles données pour l'image de sortie
    newdata = []
    for i in range(len(subdata)):
        if subdata[i][0] == 0 and subdata[i][1] == 0 and subdata[i][2] == 0:
            newdata.append((255, 255, 255, 0))
        else:
            newdata.append(ogdata[i])

    # Appliquer les nouvelles données et sauvegarder l'image
    subimage.putdata(newdata)
    subimage.save(output_path, "PNG")

    # Supprimer le dossier u2net_results
    u2net_results_path = os.path.join(test_data_path, 'u2net_results')
    if os.path.exists(u2net_results_path):
        shutil.rmtree(u2net_results_path)



def main():
    if len(sys.argv) != 3:
        print("Usage: python mon_fichier.py <src_path> <output_path>")
        sys.exit(1)
    
    src_path = sys.argv[1]
    output_path = sys.argv[2]
    
    dest_folder = os.path.join(test_data_path, 'input')
    
    # Déplacer et renommer le fichier en "input.jpg" dans le dossier de destination
    move_and_rename_file(src_path, dest_folder)
    
    # Modifier le chemin de sortie dans la fonction background_removal
    # background_removal(output_path)  # Vous devrez peut-être ajuster votre fonction pour accepter ce paramètre

    # Effectuer la suppression de l'arrière-plan
    background_removal()

if __name__ == "__main__":
    main()