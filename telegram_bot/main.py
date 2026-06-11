import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from archivos import buscar_empleado, cambiar_estado, crear_archivos, descontar_dias, guardar_solicitud
from constantes import (
    ESTADO_APROBADA,
    ESTADO_EMPLEADO_INEXISTENTE,
    ESTADO_PENDIENTE,
    ESTADO_RECHAZADA_SALDO,
    ESTADO_RECHAZADA_SUPERVISOR,
    PEDIR_DIAS,
    PEDIR_LEGAJO,
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ["BOT_TOKEN"]
SUPERVISOR_CHAT_ID = int(os.environ["SUPERVISOR_CHAT_ID"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    crear_archivos()
    await update.message.reply_text("Bienvenido al chatbot de gestión de vacaciones.\nIngrese su legajo:")
    return PEDIR_LEGAJO


async def recibir_legajo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    legajo = update.message.text.strip()

    if not legajo:
        await update.message.reply_text("El legajo no puede estar vacío. Intente nuevamente:")
        return PEDIR_LEGAJO

    empleado = buscar_empleado(legajo)

    if empleado is None:
        empleado_error = {"legajo": legajo, "nombre": "Empleado inexistente"}
        guardar_solicitud(empleado_error, 0, ESTADO_EMPLEADO_INEXISTENTE, "El legajo no existe.")
        await update.message.reply_text("No se encontró un empleado con ese legajo. Se registró el intento.")
        return ConversationHandler.END

    context.user_data["empleado"] = empleado
    await update.message.reply_text(
        f"Empleado: {empleado['nombre']}\n"
        f"Días disponibles: {empleado['dias_disponibles']}\n\n"
        "¿Cuántos días desea solicitar?"
    )
    return PEDIR_DIAS


async def recibir_dias(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    texto = update.message.text.strip()

    try:
        dias = int(texto)
        if dias <= 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text("Ingrese un número entero mayor a 0:")
        return PEDIR_DIAS

    empleado = context.user_data["empleado"]

    if dias > empleado["dias_disponibles"]:
        guardar_solicitud(empleado, dias, ESTADO_RECHAZADA_SALDO, "Saldo insuficiente.")
        await update.message.reply_text("Saldo insuficiente. Su solicitud fue rechazada.")
        return ConversationHandler.END

    id_solicitud = guardar_solicitud(empleado, dias, ESTADO_PENDIENTE, "Solicitud enviada al supervisor.")
    await update.message.reply_text("Solicitud registrada. Aguarde la aprobación del supervisor.")

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Aprobar", callback_data=f"aprobar:{id_solicitud}:{empleado['legajo']}:{dias}:{update.effective_chat.id}"),
            InlineKeyboardButton("❌ Rechazar", callback_data=f"rechazar:{id_solicitud}:{update.effective_chat.id}"),
        ]
    ])

    await context.bot.send_message(
        chat_id=SUPERVISOR_CHAT_ID,
        text=(
            f"Nueva solicitud de vacaciones\n"
            f"ID: {id_solicitud}\n"
            f"Empleado: {empleado['nombre']} (legajo {empleado['legajo']})\n"
            f"Días solicitados: {dias}"
        ),
        reply_markup=keyboard,
    )

    return ConversationHandler.END


async def supervisor_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    partes = query.data.split(":")
    accion = partes[0]
    id_solicitud = int(partes[1])
    employee_chat_id = int(partes[-1])

    if accion == "aprobar":
        legajo = partes[2]
        dias = int(partes[3])
        descontar_dias(legajo, dias)
        cambiar_estado(id_solicitud, ESTADO_APROBADA, "El supervisor aprobó la solicitud.")
        await query.edit_message_text(f"Solicitud {id_solicitud} aprobada.")
        await context.bot.send_message(chat_id=employee_chat_id, text="Tu solicitud de vacaciones fue aprobada. ¡Buen descanso!")
    else:
        cambiar_estado(id_solicitud, ESTADO_RECHAZADA_SUPERVISOR, "El supervisor rechazó la solicitud.")
        await query.edit_message_text(f"Solicitud {id_solicitud} rechazada.")
        await context.bot.send_message(chat_id=employee_chat_id, text="Tu solicitud de vacaciones fue rechazada por el supervisor.")


async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operación cancelada.")
    return ConversationHandler.END


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PEDIR_LEGAJO: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_legajo)],
            PEDIR_DIAS: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_dias)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
    )

    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(supervisor_callback))
    app.run_polling()


if __name__ == "__main__":
    main()
