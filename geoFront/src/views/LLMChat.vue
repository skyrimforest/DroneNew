<template>
  <div class="chat-container">
    <div class="messages">
      <div v-for="(msg, i) in messages" :key="i" :class="msg.role">
        <template v-if="msg.role === 'assistant'">
          <div v-if="msg.think" class="think">
            🤖 <strong>AI 思考：</strong><br />
            <pre>{{ msg.think }}</pre>
          </div>
          <div class="reply">
            💬 <strong>AI 回复：</strong>{{ msg.content }}
          </div>
        </template>
        <template v-else>
          <p><strong>你：</strong>{{ msg.content }}</p>
        </template>
      </div>
    </div>
    <div class="input-area">
      <input v-model="input" @keyup.enter="send" placeholder="请输入消息..." />
      <button @click="send">发送</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import {doHttpRequest} from "../modules/request";
const input = ref("");
const messages = ref([
  { role: "assistant", content: "你好，我是本地 AI 模型，有什么可以帮你？" },
]);

const send = async () => {
  if (!input.value.trim()) return;
  const userMsg = input.value.trim();
  messages.value.push({ role: "user", content: userMsg });
  input.value = "";

  try {
    doHttpRequest("CHAT", {
      model: "deepseek-r1:8b", // 替换成本地的模型名
      messages: messages.value.map((m) => ({
        role: m.role,
        content: m.content,
      })),
      stream: false,
    }).then((res) => {
      messages.value.push(...res.data);
    });

    const raw = res.data.message.content || "";
    const { think, reply } = extractThinkAndReply(raw);

    messages.value.push({ role: "assistant", content: reply, think });
  } catch (err) {
    console.error(err);
    messages.value.push({
      role: "assistant",
      content: "❌ 本地模型请求失败，请检查 Ollama 服务",
    });
  }
};

// 提取 <think> 标签内容和真正的回复
function extractThinkAndReply(rawText) {
  const thinkMatch = rawText.match(/<think>([\s\S]*?)<\/think>/i);
  const think = thinkMatch ? thinkMatch[1].trim() : null;
  const reply = rawText.replace(/<think>[\s\S]*?<\/think>/i, "").trim();
  return { think, reply };
}
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.messages {
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 1rem;
}
.user {
  text-align: right;
  color: #409eff;
}
.assistant {
  text-align: left;
  color: #00ffc6;
}
.think {
  font-style: italic;
  background: #393939;
  border-left: 4px solid #ccc;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  white-space: pre-wrap;
  line-height: 1.5;
}

.reply {
  margin-bottom: 1rem;
}
.input-area {
  display: flex;
  gap: 0.5rem;
}
input {
  flex: 1;
  padding: 0.5rem;
}
button {
  padding: 0.5rem 1rem;
}
</style>
