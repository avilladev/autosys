nome = input("Digite seu nome: ")
idade = int(input("Digite sua idade: "))
peso = float(input("Digite seu peso: "))
altura = float(input("Digite sua altura: "))

imc = peso / (altura * altura)

print("Seu IMC é", imc)

if imc < 18.5:
  print("Você está abaixo do peso.")
elif imc >= 18.5 and imc < 25:
  print("Você está com peso normal.")
elif imc >= 25 and imc < 30:
  print("Você está com sobrepeso.")
else:
  print("Você está obeso.")

  