from os import listdir

def main():
    print('INGRESE EL PATH DONDE DESEA REALIZAR LA BUSQUEDA')
    path = input()
    content = listdir(path)

    print(content)

if __name__ == '__main__':
    main()