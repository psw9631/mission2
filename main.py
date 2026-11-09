from default_quizzes import DEFAULT_QUIZZES

def show_menu():
    print("\n=== 나만의 퀴즈 게임 ===")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")

def read_answer():
    while True:
        text = input("정답 번호 (1~4): ").strip()

        try:
            answer = int(text)
        except ValueError:
            print("1~4 사이의 숫자를 입력하세요.")
            continue

        if 1 <= answer <= 4:
            return answer

        print("1~4 사이의 숫자를 입력하세요.")

def main():
    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "5":
            print("게임을 종료합니다.")
            break
        
        elif choice == "1":
            if not DEFAULT_QUIZZES:
                print("등록된 퀴즈가 없습니다.")
                continue
            
            correct_count = 0

            for number, quiz in enumerate(DEFAULT_QUIZZES, start=1):
                print(f"\n[문제 {number}]")
                quiz.display()
                answer = read_answer()

                if quiz.is_correct(answer):
                    correct_count += 1
                    print("정답입니다!")
                else:
                    print("오답입니다.")

            total = len(DEFAULT_QUIZZES)
            print(f"\n결과: {total}문제 중 {correct_count}문제를 맞혔어요!")

        elif choice in ("2", "3", "4"):
            print("준비 중인 기능입니다.")
        else:
            print("1~5 사이의 숫자를 입력하세요.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n게임을 종료합니다.")