class Descriptors:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        # return getattr(instance, self.name)
        return instance.__dict__[self.name]

class DescriptionAtom(Descriptors):

    valid_atom = ["C", "O", "N"]

    def __set__(self, instance, value):
        if not isinstance(instance, str):
            raise TypeError("atom must be a string ")
        instance = instance.upper()
        if instance not in type(self).valid_atom:
            raise ValueError(f"atom must be next atom: {type(self).valid_atom}")

class DescriptionBond(Descriptors):

    """
    1 - single
    2 - double
    3 - triple
    4 - aromatic
    """

    valid_bond = [1, 2, 3, 4]

    def __set__(self, instance, value):
        if instance not in type(self).valid_bond:
            raise ValueError(f"bond must be in range {type(self).valid_bond}")  # self.__class__.valid_bond

class Atom:

    atom = DescriptionAtom()

    def __init__(self, atom):
        self.atom = atom

class Molecule:

    def __init__(self):
        self._atoms = {}
        self._bonds = {}

    def add_atom(self, atom: str, n: int = None) -> None:


        if n in self._atoms:
            raise ValueError(f"atom with position {n} exist")

        elif n is None:
            n = max(self._atoms.keys()) + 1

        else:
            if not isinstance(n, int):
                raise TypeError('n must be positive integer')
            if n < 0:
                raise ValueError('n must be positive integer')
        self._atoms[n] = atom
        self._bonds[n] = {}

    def add_bonds(self, a1: int, a2: int, bond: int) -> None:

        #---------------a1, a2---------------
        if a1 not in self._atoms or a2 not in self._atoms:
            raise KeyError((f"atom at position {a1} is not found",
                            f"atom at position {a2} is not found")[a1 not in self._atoms])
        if a1 == a2:
            raise ValueError("the same atom was entered")

        if a1 not in self._bonds[a2] and a2 not in self._bonds[a1]:
            self._bonds[a1][a2] = bond  # add to one of the two, because there is will be a repetition

    def atoms(self):
        print("========= atoms  ==========")
        for key, value in (self._atoms.items()):
            print(f"{key}: {value}")

    def bonds(self):
        print("========= bonds ============")
        for key, values in (self._bonds.items()):
            for k, v in values.items():
               print(f"{key}: {k}: {v}")

    def __call__(self):
        print(f"-----{self.__class__.__name__}: start __call__  ------")
        self.atoms()
        self.bonds()
        print(f"-----{self.__class__.__name__}: end __call__  -------")

    def __str__(self):
        return f'{self.name}'


if __name__ == "__main__":
    mol = Molecule()
    atom1 = Atom("c")
    atom2 = Atom("C")
    atom3 = Atom("O")
    atom4 = Atom("n")


    mol.add_atom(atom1, n=1)
    mol.add_atom(atom2, 4)
    mol.add_atom(atom3, 2)
    mol.add_atom(atom4)

    mol.add_bonds(1, 4, 2)
    mol.add_bonds(2, 5, 1)
    print(mol.__dict__)
    print("-------------------")
    # mol.add_bonds(2, 5, 5)
    mol.atoms()
    mol.bonds()

    mol()
    print(mol.__dict__)
    print(f"-------Run code as script: {__name__ =}--------")