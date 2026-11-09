from default_quizzes import DEFAULT_QUIZZES
from quiz import Quiz

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

def add_quiz(quizzes):
    while True:
        question = input("새 문제를 입력하세요: ").strip()

        if question:
            break

        print("문제를 한 글자 이상 입력하세요.")

    choices = []

    for number in range(1, 5):
        while True:
            choice = input(f"선택지 {number}: ").strip()

            if choice:
                choices.append(choice)
                break

            print("선택지를 한 글자 이상 입력하세요.")

    answer = read_answer()
    quiz = Quiz(question, choices, answer)

    quizzes.append(quiz)
    print("퀴즈가 추가되었습니다!")

def show_quiz_list(quizzes):
    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
        return

    print(f"\n등록된 퀴즈 목록 (총 {len(quizzes)}개)")

    for number, quiz in enumerate(quizzes, start=1):
        print(f"{number}. {quiz.question}")

def main():
    quizzes = DEFAULT_QUIZZES.copy()
    best_score = None

    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "5":
            print("게임을 종료합니다.")
            break
        
        elif choice == "1":
            if not quizzes:
                print("등록된 퀴즈가 없습니다.")
                continue
            
            correct_count = 0

            for number, quiz in enumerate(quizzes, start=1):
                print(f"\n[문제 {number}]")
                quiz.display()
                answer = read_answer()

                if quiz.is_correct(answer):
                    correct_count += 1
                    print("정답입니다!")
                else:
                    print("오답입니다.")

            total = len(quizzes)
            print(f"\n결과: {total}문제 중 {correct_count}문제를 맞혔어요!")
            if best_score is None or correct_count > best_score:
                best_score = correct_count
                print("새로운 최고 기록입니다!")

        elif choice == "2":
            add_quiz(quizzes)
        elif choice == "3":
            show_quiz_list(quizzes)
        elif choice == "4":
            if best_score is None:
                print("아직 퀴즈를 푼 기록이 없습니다.")
            else:
                print(f"최고 기록: {best_score}문제 정답")
        else:
            print("1~5 사이의 숫자를 입력하세요.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n게임을 종료합니다.")