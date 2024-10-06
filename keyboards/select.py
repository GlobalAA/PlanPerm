from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_settings_keyboard(selected: list[int] = []):
	builder = InlineKeyboardBuilder()
	
	builder.add(
		InlineKeyboardButton(
			text=f"{ '☑️' if 1 in selected else ''} Відправляти повідомлення",
			callback_data=f"change_1_{selected}"
		)
	)
	builder.add(
		InlineKeyboardButton(
			text=f"{ '☑️' if 2 in selected else ''} Відправляти media",
			callback_data=f"change_2_{selected}"
		)
	)
	builder.add(
		InlineKeyboardButton(
			text=f"{ '☑️' if 3 in selected else ''} Додавати учасників ",
			callback_data=f"change_3_{selected}"
		)
	)

	builder.add(
		InlineKeyboardButton(
			text="Зберегти",
			callback_data=f"save_{selected}"
		)
	)
	
	builder.adjust(1)

	return builder.as_markup()