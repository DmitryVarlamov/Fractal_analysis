from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt

delta = [1, 2]
CELL_SIZES = np.arange(5, 30)

def convert_image(image, converted_file_name):
    black_and_white = image.convert('1')
    black_and_white.save(converted_file_name)
    return black_and_white

def get_A(cell, ds):
    length, width = cell.size[0], cell.size[1]
    u = np.zeros((len(ds) + 1, length + 1, width + 1))
    b = np.zeros((len(ds) + 1, length + 1, width + 1))
    v = np.zeros((len(ds) + 1))
    A = np.zeros((len(ds) + 1))

    for i in range(0, length):
        for j in range(0, width):
            u[0][i][j] = cell.getpixel((i, j))
            b[0][i][j] = cell.getpixel((i, j))

            for d in ds:
                u[d][i][j] = max(u[d - 1][i][j] + 1, max(u[d - 1][i + 1][j + 1], u[d - 1][i - 1][j + 1], u[d - 1][i + 1][j - 1], u[d - 1][i - 1][j - 1]))
                b[d][i][j] = min(b[d - 1][i][j] - 1, min(b[d - 1][i + 1][j + 1], b[d - 1][i - 1][j + 1], b[d - 1][i + 1][j - 1], b[d - 1][i - 1][j - 1]))
    
    for d in ds:
        v[d] = 0
        for i in range(0, length):
            for j in range(0, width):
                v[d] += u[d][i][j] - b[d][i][j]
    
    for d in ds:
        A[d] = (v[d] - v[d-1]) / 2
    
    return A

def count_dimension(image, cell_size):
    length, width = image.size[0], image.size[1]
    cell_length, cell_width = length//cell_size, width//cell_size
    A = np.zeros((cell_length, cell_width, len(delta)+1))
    for i in range(0, cell_length):
        for j in range(0, cell_width):
            area = (i*cell_size, j*cell_size, (i+1)*cell_size, (j+1)*cell_size)
            cell = image.crop(area)
            for d in delta:
                A[i][j][d] = get_A(cell, delta)[d]

    
    As = []
    for d in delta:
        s = 0
        for i in range(0, cell_length):
            for j in range(0, cell_width):
                s += A[i][j][d]
        As.append(s)
        
    return 2 - np.polyfit(np.log(As), np.log(delta), 1)[0] * (-1)

def get_graph_data(image):
    data = []
    for cell_size in CELL_SIZES:
        image_copy = image
        data.append(count_dimension(image_copy, cell_size))

    return data



if __name__ == '__main__':
    finished = False
    while not finished:
        print("Please, type the name of the file. Or press enter to skip. Default name is image.jpg\n You can type multiple file names, separated by space\n Example: 'image1.jpg image2.jpg image3.jpg'")
        names = input()
        if not names:
            names = ['image.jpg']
        else:
            names = names.split(' ')
        try:
            plt.cla()
            fig, ax = plt.subplots()
            for name in names:
                im = Image.open(name)
                im = convert_image(im, 'inverted_' + name)
                file_data = get_graph_data(im)
                ax.plot(CELL_SIZES, file_data, label = name)

            ax.set_xlabel('cell size')
            ax.set_ylabel('Dimension')
            ax.legend()
            fig.savefig("result_graph.png")
            finished = True
        except Exception as e:
            print(e)
            print("Could not find the file. Please try again.")