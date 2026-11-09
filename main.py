import json
from pathlib import Path
from default_quizzes import DEFAULT_QUIZZES
from quiz import Quiz

class QuizGame:
    def __init__(self):
        self.quizzes = DEFAULT_QUIZZES.copy()
        self.best_score = None
        self.load_state()

    def show_menu(self):
        print("\n=== 나만의 퀴즈 게임 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        correct_count = 0

        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[문제 {number}]")
            quiz.display()
            answer = read_answer()

            if quiz.is_correct(answer):
                correct_count += 1
                print("정답입니다!")
            else:
                print("오답입니다.")

        total = len(self.quizzes)
        print(f"\n결과: {total}문제 중 {correct_count}문제를 맞혔어요!")

        if self.best_score is None or correct_count > self.best_score:
            self.best_score = correct_count
            self.save_state()
            print("새로운 최고 기록입니다!")

    def add_quiz(self):
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

        self.quizzes.append(quiz)
        self.save_state()
        print("퀴즈가 추가되었습니다!")

    def show_quiz_list(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")

        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"{number}. {quiz.question}")

    def show_best_score(self):
        if self.best_score is None:
            print("아직 퀴즈를 푼 기록이 없습니다.")
        else:
            print(f"최고 기록: {self.best_score}문제 정답")

    def save_state(self):
        quiz_data = []

        for quiz in self.quizzes:
            quiz_data.append({
                "question": quiz.question,
                "choices": quiz.choices,
                "answer": quiz.answer,
            })

        state = {
            "quizzes": quiz_data,
            "best_score": self.best_score,
        }

        state_path = Path(__file__).resolve().with_name("state.json")

        try:
            with state_path.open("w", encoding="utf-8") as file:
                json.dump(state, file, ensure_ascii=False, indent=4)
        except OSError as error:
            print(f"저장하지 못했습니다. {error}")

    def load_state(self):
        state_path = Path(__file__).resolve().with_name("state.json")

        try:
            with state_path.open("r", encoding="utf-8") as file:
                state = json.load(file)

            quiz_items = state["quizzes"]
            if not isinstance(quiz_items, list):
                raise ValueError("퀴즈 목록은 리스트여야 합니다.")

            quizzes = []
            for item in quiz_items:
                question = item["question"]
                choices = item["choices"]
                answer = item["answer"]

                if not isinstance(question, str) or not question.strip():
                    raise ValueError("문제 문장이 비어 있거나 잘못되었습니다.")

                if not isinstance(choices, list) or len(choices) != 4:
                    raise ValueError("선택지는 4개여야 합니다.")

                for choice in choices:
                    if not isinstance(choice, str) or not choice.strip():
                        raise ValueError("선택지는 비어 있지 않은 문자열이어야 합니다.")

                if type(answer) is not int or not 1 <= answer <= 4:
                    raise ValueError("정답 번호는 1~4 사이의 정수여야 합니다.")

                quizzes.append(Quiz(question, choices, answer))

            best_score = state["best_score"]
            if best_score is not None:
                if type(best_score) is not int or best_score < 0:
                    raise ValueError("최고 점수는 0 이상의 정수여야 합니다.")
                
        except FileNotFoundError:
            return
        except (OSError, ValueError, KeyError, TypeError):
            print("저장 파일을 불러올 수 없어 기본 문제로 시작합니다.")
            return

        self.quizzes = quizzes
        self.best_score = best_score

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
    game = QuizGame()
    
    while True:
        game.show_menu()
        choice = input("선택: ").strip()

        if choice == "5":
            print("게임을 종료합니다.")
            break
        
        elif choice == "1":
            game.play_quiz()
        elif choice == "2":
            game.add_quiz()
        elif choice == "3":
            game.show_quiz_list()
        elif choice == "4":
            game.show_best_score()
        else:
            print("1~5 사이의 숫자를 입력하세요.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n게임을 종료합니다.")