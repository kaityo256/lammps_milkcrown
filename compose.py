import sys


class MyDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


def read_atoms(f, h):
    atoms = [[] for _ in range(h.num_atoms)]
    LX = h.xe - h.xs
    LY = h.ye - h.ys
    LZ = h.ze - h.zs
    while True:
        line = f.readline()
        if 'ITEM: TIMESTEP' in line:
            return atoms
        id, _, x, y, z = line.split()
        id = int(id) - 1
        x = h.xs + LX * float(x)
        y = h.ys + LY * float(y)
        z = h.ys + LZ * float(z)
        atoms[id] = (x, y, z)


def save_file(filename, atoms):
    with open(filename, "w") as f:
        f.write("Position Data\n\n")
        f.write(f"{len(atoms)} atoms\n")
        f.write("1 atom types\n\n")
        f.write("-60.00 40.00 xlo xhi\n")
        f.write("-40.00 40.00 ylo yhi\n")
        f.write("-40.00 40.00 zlo zhi\n")
        f.write("\n")
        f.write("Atoms\n\n")
        for i in range(len(atoms)):
            x, y, z = atoms[i]
            f.write(f"{i+1} 1 {x} {y} {z}\n")
        f.write("\n")
        f.write("Velocities\n\n")
        for i in range(len(atoms)):
            f.write(f"{i+1} 0 0 0\n")


def readdata(f):
    h = MyDict()
    while True:
        line = f.readline()
        if 'ITEM: NUMBER OF ATOMS' in line:
            # 原子数の取得
            num_atoms = int(f.readline())
            h.num_atoms = num_atoms
        if 'ITEM: BOX BOUNDS' in line:
            # シミュレーションボックスの取得
            xs, xe = f.readline().split()
            ys, ye = f.readline().split()
            zs, ze = f.readline().split()
            h.xs = float(xs)
            h.xe = float(xe)
            h.ys = float(ys)
            h.ye = float(ye)
            h.zs = float(zs)
            h.ze = float(ze)
        if 'ITEM: ATOMS' in line:
            return read_atoms(f, h)


def main():
    if len(sys.argv) != 4:
        print("usage: python3 composite.py droplet wall output.atoms")
        exit()
    droplet_file = sys.argv[1]
    wall_file = sys.argv[2]
    output_file = sys.argv[3]
    with open(droplet_file) as f:
        droplet_atoms = readdata(f)
    with open(wall_file) as f:
        wall_atoms = readdata(f)
    for i in range(len(droplet_atoms)):
        (x, y, z) = droplet_atoms[i]
        droplet_atoms[i] = (x - 40, y, z)
    atoms = droplet_atoms + wall_atoms
    save_file(output_file, atoms)


if __name__ == '__main__':
    main()
