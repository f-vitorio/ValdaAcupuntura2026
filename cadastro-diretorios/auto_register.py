#!/usr/bin/env python3
"""
Automação de cadastro em diretórios - Valda Acupuntura
Preenche formulários automaticamente, pausa para CAPTCHA/envio manual.
"""

import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ============================================================
# DADOS DO NEGÓCIO
# ============================================================

BUSINESS = {
    "name": "Valda Acupuntura",
    "professional": "Dra. Valda Fernandes",
    "street": "Rua Maquerobi",
    "number": "156",
    "neighborhood": "Vila da Saúde",
    "city": "São Paulo",
    "state": "SP",
    "cep": "04053-030",
    "phone": "(11) 98313-4656",
    "phone_clean": "11983134656",
    "whatsapp": "(11) 98313-4656",
    "email": "valdaacupuntura@gmail.com",
    "website": "https://valdaacupuntura.com.br/",
    "category": "Acupuntura",
    "subcategory": "Medicina Tradicional Chinesa",
    "description": "Clínica de acupuntura em São Paulo com 20 anos de experiência. Atendimento 100% individual, 4,8★ no Google (132+ avaliações).",
    "hours": "Segunda a Sexta, 08h às 19h",
    "full_address": "Rua Maquerobi, 156 - Vila da Saúde, São Paulo - SP, 04053-030",
}

# ============================================================
# CONFIGURAÇÃO DO BROWSER
# ============================================================

def create_driver(headed=True):
    """Cria driver Chrome com configurações otimizadas."""
    options = Options()
    if headed:
        options.add_argument("--start-maximized")
    else:
        options.add_argument("--headless=new")
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def safe_fill(driver, selector, value, by=By.CSS_SELECTOR, timeout=10):
    """Preenche campo de forma segura."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        element.clear()
        element.send_keys(value)
        return True
    except (TimeoutException, NoSuchElementException) as e:
        print(f"  ⚠️  Não foi possível preencher '{selector}': {e}")
        return False

def safe_click(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    """Clica em elemento de forma segura."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, selector))
        )
        element.click()
        return True
    except (TimeoutException, NoSuchElementException) as e:
        print(f"  ⚠️  Não foi possível clicar '{selector}': {e}")
        return False

def select_option(driver, selector, value, by=By.CSS_SELECTOR, timeout=10):
    """Seleciona opção em dropdown."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        select = Select(element)
        select.select_by_visible_text(value)
        return True
    except Exception as e:
        print(f"  ⚠️  Não foi possível selecionar '{selector}': {e}")
        return False

def wait_for_user(message="Resolva o CAPTCHA e clique em ENVIAR"):
    """Pausa para ação manual do usuário."""
    print(f"\n{'='*60}")
    print(f"⏸️  PAUSA: {message}")
    print(f"{'='*60}")
    print("Pressione ENTER quando concluir...")
    input()
    print("✅ Continuando...\n")

def take_screenshot(driver, name):
    """Salva screenshot."""
    path = f"/home/fvitorio/Documents/PROJETOS/ValdaAcupuntura2026/cadastro-diretorios/{name}.png"
    driver.save_screenshot(path)
    print(f"  📸 Screenshot salvo: {name}.png")

# ============================================================
# CADASTRO: BING PLACES
# ============================================================

def register_bing_places(driver):
    """Cadastra no Bing Places."""
    print("\n" + "="*60)
    print("🔴 BING PLACES - Cadastro")
    print("="*60)
    
    driver.get("https://www.bingplaces.com/")
    time.sleep(3)
    
    print("  📍 Página carregada")
    take_screenshot(driver, "bing_01_home")
    
    # Procurar botão de cadastro
    try:
        # Tentar encontrar "Get Started" ou similar
        buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'Start') or contains(text(), 'Get') or contains(text(), 'Cadastr')]")
        if buttons:
            print(f"  🔍 Encontrados {len(buttons)} botões de cadastro")
            for i, btn in enumerate(buttons):
                print(f"    - Botão {i}: {btn.text}")
        
        # Procurar link "Add your business"
        links = driver.find_elements(By.XPATH, "//a[contains(@href, 'add') or contains(@href, 'register') or contains(@href, 'signup')]")
        if links:
            print(f"  🔍 Encontrados {len(links)} links de cadastro")
            for i, link in enumerate(links):
                print(f"    - Link {i}: {link.get_attribute('href')}")
        
    except Exception as e:
        print(f"  ⚠️  Erro ao buscar elementos: {e}")
    
    # Tentar login com Microsoft
    print("\n  📝 Próximo passo: Faça login com sua conta Microsoft")
    wait_for_user("Faça login no Bing Places e navegue até 'Add a new business'")
    
    # Após login, preencher formulário
    print("  📝 Preenchendo dados do negócio...")
    
    # Nota: Os seletores abaixo são estimativas - podem precisar de ajuste
    # baseado na estrutura real da página após login
    
    safe_fill(driver, "[id*='name'], [name*='name'], input[placeholder*='Business name']", BUSINESS["name"])
    safe_fill(driver, "[id*='address'], [name*='address'], input[placeholder*='Address']", BUSINESS["full_address"])
    safe_fill(driver, "[id*='phone'], [name*='phone'], input[placeholder*='Phone']", BUSINESS["phone"])
    safe_fill(driver, "[id*='website'], [name*='website'], input[placeholder*='Website']", BUSINESS["website"])
    safe_fill(driver, "[id*='email'], [name*='email'], input[placeholder*='Email']", BUSINESS["email"])
    
    take_screenshot(driver, "bing_02_form_preenchido")
    
    print("\n  ✅ Formulário preenchido!")
    wait_for_user("Revise os dados, resolva CAPTCHA e clique em ENVIAR")
    
    take_screenshot(driver, "bing_03_enviado")
    print("  ✅ Bing Places concluído!")

# ============================================================
# CADASTRO: WAZE
# ============================================================

def register_waze(driver):
    """Cadastra no Waze."""
    print("\n" + "="*60)
    print("🔴 WAZE - Cadastro")
    print("="*60)
    
    driver.get("https://business.waze.com/")
    time.sleep(3)
    
    print("  📍 Página carregada")
    take_screenshot(driver, "waze_01_home")
    
    # Procurar botão de cadastro
    try:
        buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'Add') or contains(text(), 'Submit') or contains(text(), 'Cadastr')]")
        if buttons:
            print(f"  🔍 Encontrados {len(buttons)} botões")
            for btn in buttons:
                print(f"    - {btn.text}")
    except Exception as e:
        print(f"  ⚠️  Erro: {e}")
    
    print("\n  📝 Próximo passo: Clique em 'Add your business'")
    wait_for_user("Navegue até o formulário de cadastro no Waze")
    
    # Preencher formulário
    print("  📝 Preenchendo dados...")
    
    safe_fill(driver, "input[name*='name'], input[placeholder*='name'], #business-name", BUSINESS["name"])
    safe_fill(driver, "input[name*='address'], input[placeholder*='address'], #address", BUSINESS["full_address"])
    safe_fill(driver, "input[name*='phone'], input[placeholder*='phone'], #phone", BUSINESS["phone"])
    safe_fill(driver, "input[name*='website'], input[placeholder*='website'], #website", BUSINESS["website"])
    
    take_screenshot(driver, "waze_02_form_preenchido")
    
    print("\n  ✅ Formulário preenchido!")
    wait_for_user("Revise, resolva CAPTCHA e clique em ENVIAR")
    
    take_screenshot(driver, "waze_03_enviado")
    print("  ✅ Waze concluído!")

# ============================================================
# CADASTRO: GUIA MAIS
# ============================================================

def register_guia_mais(driver):
    """Cadastra no Guia Mais."""
    print("\n" + "="*60)
    print("🟡 GUIA MAIS - Cadastro")
    print("="*60)
    
    driver.get("https://www.guiamais.com.br/")
    time.sleep(3)
    
    print("  📍 Página carregada")
    take_screenshot(driver, "guia_mais_01_home")
    
    # Procurar link de cadastro
    try:
        links = driver.find_elements(By.XPATH, "//a[contains(text(), 'Cadastr') or contains(text(), 'Anunc') or contains(@href, 'anuncie')]")
        if links:
            print(f"  🔍 Encontrados {len(links)} links de cadastro")
            for link in links:
                print(f"    - {link.text}: {link.get_attribute('href')}")
                link.click()
                time.sleep(3)
                break
    except Exception as e:
        print(f"  ⚠️  Erro: {e}")
    
    # Tentar URL direta
    driver.get("https://www.guiamais.com.br/anuncie")
    time.sleep(3)
    
    take_screenshot(driver, "guia_mais_02_formulario")
    
    # Preencher formulário
    print("  📝 Preenchendo dados...")
    
    safe_fill(driver, "input[name*='name'], input[name*='nome'], #businessName", BUSINESS["name"])
    safe_fill(driver, "input[name*='address'], input[name*='endereco'], #address", BUSINESS["full_address"])
    safe_fill(driver, "input[name*='cep'], #cep", BUSINESS["cep"])
    safe_fill(driver, "input[name*='phone'], input[name*='telefone'], #phone", BUSINESS["phone"])
    safe_fill(driver, "input[name*='email'], #email", BUSINESS["email"])
    safe_fill(driver, "input[name*='website'], input[name*='site'], #website", BUSINESS["website"])
    
    # Tentar selecionar categoria
    select_option(driver, "select[name*='category'], select[name*='categoria']", "Saúde")
    
    take_screenshot(driver, "guia_mais_03_form_preenchido")
    
    print("\n  ✅ Formulário preenchido!")
    wait_for_user("Revise, resolva CAPTCHA e clique em ENVIAR")
    
    take_screenshot(driver, "guia_mais_04_enviado")
    print("  ✅ Guia Mais concluído!")

# ============================================================
# MAIN
# ============================================================

def main():
    print("="*60)
    print("🚀 AUTOMAÇÃO DE CADASTRO EM DIRETÓRIOS")
    print("   Valda Acupuntura")
    print("="*60)
    
    print("\n📋 Dados do negócio:")
    print(f"   Nome: {BUSINESS['name']}")
    print(f"   Endereço: {BUSINESS['full_address']}")
    print(f"   Telefone: {BUSINESS['phone']}")
    print(f"   Email: {BUSINESS['email']}")
    print(f"   Website: {BUSINESS['website']}")
    
    print("\n🔧 Iniciando browser...")
    driver = create_driver(headed=True)
    
    try:
        # Menu de opções
        print("\n" + "="*60)
        print("Escolha o diretório para cadastrar:")
        print("="*60)
        print("1. Bing Places (RECOMENDADO - maior impacto)")
        print("2. Waze")
        print("3. Guia Mais")
        print("4. Todos (sequencial)")
        print("0. Sair")
        
        choice = input("\nOpção: ").strip()
        
        if choice == "1":
            register_bing_places(driver)
        elif choice == "2":
            register_waze(driver)
        elif choice == "3":
            register_guia_mais(driver)
        elif choice == "4":
            register_bing_places(driver)
            register_waze(driver)
            register_guia_mais(driver)
        elif choice == "0":
            print("Saindo...")
            return
        else:
            print("Opção inválida!")
            return
        
        print("\n" + "="*60)
        print("✅ PROCESSO CONCLUÍDO!")
        print("="*60)
        print("\n📸 Screenshots salvos em: cadastro-diretorios/")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Processo interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        take_screenshot(driver, "erro")
    finally:
        print("\n🔌 Fechando browser...")
        driver.quit()

if __name__ == "__main__":
    main()
