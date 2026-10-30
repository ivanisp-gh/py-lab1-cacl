import sys

from toolkit.calculator import calculation
from toolkit.converter import convert
from toolkit.errors import ToolkitError


def main() -> None:
    argv = sys.argv[1:]

    if not argv or argv[0] == "--help":
        print("Использование: python -m toolkit <команда> [аргументы]")
        print("Команды: calc EXPRESSION | convert VALUE --from UNIT --to UNIT | --help")
        print("Пример: python -m toolkit convert 80 --from mm --to cm")
        sys.exit(0)

    command = argv[0]
    args = argv[1:]

    try:
        if command == "calc":
            if not args:
                raise ToolkitError("Укажите выражение для calc")
            expression = " ".join(args)
            result = calculation(expression)
            print(result)

        elif command == "convert":
            if not args:
                raise ToolkitError("Укажите значение для convert")
            if "--from" in args or "--to" in args:
                if args.count("--from") != 1 or args.count("--to") != 1 or len(args) != 5:
                    raise ToolkitError("Использование: convert VALUE --from UNIT --to UNIT")
                try:
                    from_idx = args.index("--from")
                    to_idx = args.index("--to")
                    from_unit = args[from_idx + 1]
                    to_unit = args[to_idx + 1]
                    used = {from_idx, from_idx + 1, to_idx, to_idx + 1}
                    values = [a for i, a in enumerate(args) if i not in used]
                    if len(values) != 1 or from_unit.startswith("--") or to_unit.startswith("--"):
                        raise ToolkitError("Использование: convert VALUE --from UNIT --to UNIT")
                    value = values[0]
                except IndexError:
                    raise ToolkitError("Использование: convert VALUE --from UNIT --to UNIT")
                result = convert(f"{value}{from_unit}", to_unit)
            else:
                if len(args) != 1:
                    raise ToolkitError("Использование: convert VALUE с единицей измерения")
                value_with_unit = args[0]
                result = convert(value_with_unit)
            print(result)

        else:
            raise ToolkitError(f"Неизвестная команда: {command}")

    except (ToolkitError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()