def show_menu():
    print("\n=== 나만의 퀴즈 게임 ===")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")


def main():
    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "5":
            print("게임을 종료합니다.")
            break
        elif choice in ("1", "2", "3", "4"):
            print("준비 중인 기능입니다.")
        else:
            print("1~5 사이의 숫자를 입력하세요.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n게임을 종료합니다.")