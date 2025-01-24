import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from ctransformers import AutoModelForCausalLM

class ZenasBot:
    def __init__(self, telegram_token):
        # Initialize the bot with your telegram token
        self.application = Application.builder().token(telegram_token).build()
        
        # Initialize Llama 2 model
        # Note: You'll need to download the model file separately
        self.llm = AutoModelForCausalLM.from_pretrained(
            "TheBloke/Llama-2-7B-Chat-GGUF",
            model_file="llama-2-7b-chat.Q4_K_M.gguf",
            model_type="llama",
            max_new_tokens=512,
            temperature=0.7
        )
        
        # Set up command handlers
        self.setup_handlers()
    
    def setup_handlers(self):
        """Set up message and command handlers"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /start is issued."""
        await update.message.reply_text(
            "Hello! I'm Zenas, your AI assistant. How can I help you today?"
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /help is issued."""
        help_text = """
        Here are the available commands:
        /start - Start the conversation
        /help - Show this help message
        
        You can also just send me any message and I'll respond!
        """
        await update.message.reply_text(help_text)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages and generate responses using the LLM."""
        user_message = update.message.text
        
        # Show typing indicator
        await update.message.chat.send_action(action="typing")
        
        try:
            # Generate response using Llama 2
            prompt = f"USER: {user_message}\nASSISTANT:"
            response = self.llm(prompt)
            
            # Send the response
            await update.message.reply_text(response)
            
        except Exception as e:
            error_message = "I apologize, but I encountered an error processing your message. Please try again."
            await update.message.reply_text(error_message)
            print(f"Error: {str(e)}")
    
    def run(self):
        """Run the bot until the user presses Ctrl-C"""
        self.application.run_polling()

def main():
    # Replace with your Telegram bot token
    TELEGRAM_TOKEN = "7325536944:AAFcEnPchIHczsPaSXzDqaBFGkc3praPLFk"
    
    # Create and run the bot
    bot = ZenasBot(TELEGRAM_TOKEN)
    print("Bot is running... Press Ctrl-C to stop.")
    bot.run()

if __name__ == "__main__":
    main()