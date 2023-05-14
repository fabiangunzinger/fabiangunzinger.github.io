---
title: "Evolving notes on learning vim"
date: 2023-05-13T23:50:36+01:00
draft: false
---

A back-of-the-envelope calculation suggests that I've spend about 120 hours configuring nvim over the past two months. That's right, 120 hours! And I'm still not done, and there are still some things about the configuration I don't fully understand (why, for instance, does the `config` argument of the lazy.nvim plugin manager take a function rather than a table?).

Most of the time, though, I've really loved working on it. In fact, is started out entirely as a hobby project during a self-prescribed break from intense learning. At some point I realised that getting the debug workflow setup would really help my work, which added a bit of pressure to make progress fast, but on the whole, I really enjoyed the time I spend on it, and have enjoyed learning a bit of Lua in the process.

Why bother with vim in the first place? My PyCharm using colleagues certainly don't understand, and they are in good company. For me, there are two main arguments: First, I do believe that while learning the basic tools of the trade (vim, bash commands, etc.) requires some investment, they ultimately help me become better and more productive at my job than if I relied on tools that work out of the box, mainly because they are more versatile and can easily be extended and customised to the problems at hand, in a way out-of-the-box tools cannot be. Second, I derive immense satisfaction from the sense of craftsmanship they provide -- configuring vim feels akin to a woodworker who crafts his own tools and becomes intimately familiar with them in the process. Come to think of it, there are more reasons: I have the nervous blinking interfaces of IDEs, and the fact that I mindlessly click around without needing to understand how things work under the hood -- it's time-saving in the short-run, yes, but also robs me of understanding that using vim effectively requires me to acquire (which, mind you, can be frustrating when you just want to get something done quickly). And then, finally, there is the fact that I've been dabbling with vim for many years now, almost 10. And while I haven't ever used it on a regular basis up recently, I have invested a lot of time on occasion to improve my skills. So, there is a sense that all this time would have been wasted if I were to switch away from it now. As a trained economist, I'm not supposed to care about sunk costs. But part of me does, especially because I believe that my investments place me at a point from where I can become very productive very quickly now, if only I persevere (which, even economists would agree, means I probably shouldn't stop).

The thing is, though: it looks like the value of programming skills might drop rather dramatically rather soon. I'm writing elsewhere about the impact of recent AI advances of my thoughts on my work more broadly. Here, I solely want to record my thoughts about the usefulness of investing in mastering vim.

The core of the argument for investing in mastering vim is that while it slows me down in the short run, it will make me faster in the long-run. But what if in the long-run, I'm not coding any longer because almost nobody is? 

Should this change things? In the face of rapidly improving advances in AI and with serious people[^eloundou2023gpt] telling us that coding is among the skills that is most likely to be automated away by current AI technology and its offshoots, what's the point of investing in becoming good at it now?


[^eloundou2023gpt]: https://arxiv.org/pdf/2303.10130.pdf. 

