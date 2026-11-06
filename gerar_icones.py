#!/usr/bin/env python3
"""Gera todos os ícones do PWA a partir de uma imagem base. Requer Pillow: pip install Pillow"""
from PIL import Image
import os

os.makedirs('icons', exist_ok=True)

# Nome do arquivo da imagem original que você enviou
ARQUIVO_ORIGINAL = 'logo_original.png' 

try:
    # Abre a imagem original e converte para RGBA (para manter transparência se houver)
    img_original = Image.open(ARQUIVO_ORIGINAL).convert('RGBA')
except FileNotFoundError:
    print(f"❌ Erro: O arquivo '{ARQUIVO_ORIGINAL}' não foi encontrado.")
    print("Salve a imagem enviada na mesma pasta do script com esse nome.")
    exit(1)

def gerar_icone(size, nome_arquivo):
    # Redimensiona a imagem para o tamanho desejado usando um filtro de alta qualidade
    img_redimensionada = img_original.resize((size, size), Image.Resampling.LANCZOS)
    img_redimensionada.save(f'icons/{nome_arquivo}')
    print(f"✅ Gerado: icons/{nome_arquivo} ({size}x{size})")

# Gera os ícones nos tamanhos padrão do PWA
gerar_icone(192, 'icon-192.png')
gerar_icone(512, 'icon-512.png')
gerar_icone(64, 'favicon.png')

# Para o ícone maskable, o recomendado é ter a arte centralizada.
# Como a sua imagem já tem uma moldura, vamos apenas redimensionar para 512.
# (Se precisar de margem extra, você pode adicionar padding depois, mas a arte ficará menor)
gerar_icone(512, 'icon-512-maskable.png')

print('\n🎉 Todos os ícones foram gerados na pasta ./icons/')