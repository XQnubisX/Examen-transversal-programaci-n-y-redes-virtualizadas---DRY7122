vlan = int(input("Ingrese el número de VLAN: "))

if 1 <= vlan <= 1005:
    print("La VLAN ingresada está en el rango normal.")
elif 1006 <= vlan <= 4094:
    print("La VLAN ingresada está en el rango extendido.")
else:
    print("Número de VLAN inválido.")
