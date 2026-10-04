class Usuario:
    ROLES_PERMITIDOS = ("Administrador", "Empleado", "Cliente")

    def __init__(self, identificador, nombre, usuario, contrasena, rol="Cliente"):
        self.identificador = identificador
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

    @staticmethod
    def validar_texto(valor, campo):
        # Reutiliza una validacion basica para datos obligatorios.
        if not valor or not valor.strip():
            raise ValueError(f"El campo {campo} no puede estar vacio.")

        return valor.strip()

    @property
    def identificador(self):
        return self._identificador

    @identificador.setter
    def identificador(self, valor):
        self._identificador = self.validar_texto(valor, "identificador")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = self.validar_texto(valor, "nombre")

    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, valor):
        self._usuario = self.validar_texto(valor, "usuario")

    @property
    def contrasena(self):
        return self._contrasena

    @contrasena.setter
    def contrasena(self, valor):
        self._contrasena = self.validar_texto(valor, "contrasena")

    @property
    def rol(self):
        return self._rol

    @rol.setter
    def rol(self, valor):
        rol_validado = self.validar_texto(valor, "rol")
        if rol_validado not in self.ROLES_PERMITIDOS:
            raise ValueError("El rol seleccionado no es valido.")

        self._rol = rol_validado
