import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import sympy as sp

def solver():
    eq = e1.get().strip()
    if '=' not in eq:
        result.config(text="Ошибка: добавь '='", fg="red")
        return

    try:
        left, right = eq.split('=', 1)
        left_expr = sp.parse_expr(left.strip())
        right_expr = sp.parse_expr(right.strip())

        equation = sp.Eq(left_expr, right_expr)
        solution = sp.solve(equation, dict=True)

        if solution:
            result.config(text=f"Решение: {solution}", fg="darkgreen")
        else:
            result.config(text="Нет решений или бесконечное множество", fg="orange")
    except Exception as err:
        result.config(text=f"Ошибка: {str(err)[:60]}...", fg="red")


def showplot():
    eq = e1.get().strip()
    if '=' not in eq:
        result.config(text="Ошибка: добавь '='", fg="red")
        return

    try:
        left, right = eq.split('=', 1)
        # f(x) = left (левая часть уравнения) - right (правая часть уравнения)
        expr = sp.parse_expr(left.strip()) - sp.parse_expr(right.strip())

        # Главная переменная это x
        x = sp.symbols('x')
        f = sp.lambdify(x, expr, 'numpy')

        # Диапазон для графика
        x_vals = np.linspace(-10, 10, 400)
        y_vals = f(x_vals)

        # Строение графика
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, linewidth=3, color='#1c90ba', label=f'f(x) = {expr}')
        plt.title(f'График уравнения: {eq}', fontsize=14)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.axhline(0, color='black', linewidth=1)  # ось X
        plt.axvline(0, color='black', linewidth=1)  # ось Y

        # Корни уравнения (где f(x)=0)
        roots = sp.solve(expr, x)
        for root in roots:
            if root.is_real:
                r = float(root)
                plt.scatter([r], [0], color='red', s=50, zorder=5)
                plt.annotate(f'Корень: x={r:.2f}', xy=(r, 0), xytext=(r + 0.5, 1))

        plt.tight_layout()
        plt.show()

    except Exception as err:
        result.config(text=f"Не могу построить график\n{str(err)[:100]}", fg="red")
# Интерфейс
w = Tk()
w.title("Решатель уравнений + Графики")
w.geometry("480x280")
w.configure(bg="#8ab7ff")

Label(w, text="Введите уравнение (например: x**2 - 5*x + 6 = 0):",
      font=('Sitka Small', 11), bg='#8ab7ff').pack(pady=10)

e1 = Entry(w, font=('Sitka Small', 13), width=34, bg='white')
e1.pack(pady=5)

Button(w, text="Решить уравнение", command=solver,
       font=('Sitka Small', 12), bg='#6ea4fa', width=20).pack(pady=8)

Button(w, text="Показать график", command=showplot,
       font=('Sitka Small', 12), bg='#6ea4fa', width=20).pack(pady=5)

result = Label(w, text='', font=('Sitka Small', 11), bg='#8ab7ff', wraplength=450, height=3)
result.pack()

w.mainloop()
