from app.core.config import settings
from app.core.logging import logger
from app.services.utils import call_api
from google import genai
from google.genai import types
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from contextlib import AsyncExitStack
from typing import List


class ChatBot:
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.session: ClientSession = None
        self.available_tools: List = []
        self.available_resources: List = []


    async def find_mcp_server(self, query: str, chat_history: List[dict]):
        conversation = chat_history + [{'role': 'user', 'content': query}]
        mcp_server_url = await call_api(settings.AI_UTILS_API_URL + "/find_mcp", {"messages": conversation})
        return mcp_server_url


    async def connect_to_server(self, mcp_server_url: str):
        try:
            streamable_transport = await self.exit_stack.enter_async_context(
                streamablehttp_client(url=mcp_server_url)
            )
            read, write, _ = streamable_transport 
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(read, write)
            )
            await self.session.initialize()
            
            tools_response = await self.session.list_tools()
            for tool in tools_response.tools:
                self.available_tools.append(
                    types.FunctionDeclaration(
                        name=tool.name,
                        description=tool.description,
                        parameters=tool.inputSchema
                    )
                )

                logger.info

            resources_response = await self.session.list_resources()
            if resources_response and resources_response.resources:
                for resource in resources_response.resources:
                    resource_uri = str(resource.uri)
                    self.available_resources.append(resource_uri)
                
        except Exception as e:
            logger.error(e, exc_info=True)

    
    async def process_query(self, query, chat_history):
        history = []
        for message in chat_history:
            history.append(
                types.Content(
                    role=message['role'],
                    parts=[{"text": message['content']}]
                )
            )

        tools = types.Tool(function_declarations=self.available_tools)

        chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="Bạn là một trợ lý ảo.",
                temperature=0.0,
                tools=[tools],
            ),
            history=history
        )

        response = chat.send_message(query)
            
        if response.function_calls:
            result = await self.session.call_tool(response.function_calls[0].name, arguments=response.function_calls[0].args)
            return str(result)

        return response.text

    async def cleanup(self):
        await self.exit_stack.aclose()


async def get_response(query, chat_history, service, chat_id):
    chatbot = ChatBot()
    await chatbot.connect_to_server()
    response = await chatbot.process_query(query.query, query.chat_history)
    await chatbot.cleanup()