const { ActivityHandler, BotFrameworkAdapter } = require('botbuilder');

class MyBot extends ActivityHandler {
constructor() {
super();
this.onMessage(async (context, next) => {
await context.sendActivity(`You said '${context.activity.text}'`);
await next();
});
}
}

const adapter = new BotFrameworkAdapter({
appId: process.env.MicrosoftAppId,
appPassword: process.env.MicrosoftAppPassword
});

const bot = new MyBot();
adapter.processActivity(req, res, async (context) => {
await bot.run(context);
});
