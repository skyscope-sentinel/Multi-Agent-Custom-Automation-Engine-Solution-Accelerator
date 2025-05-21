"""Tools for the Knowledge agent to interact with Azure AI Search or file search."""
import json
import logging
import os
from typing import Any, Dict, List, Optional, Annotated, Union

from app_config import config
from azure.core.exceptions import HttpResponseError
from azure.search.documents import SearchClient
from semantic_kernel.functions import kernel_function
from models.messages_kernel import AgentType

class KnowledgeTools:
    """Tools for the Knowledge agent to interact with Azure AI Search or files."""
    
    # Define formatting instructions
    formatting_instructions = "Instructions: returning the output of this function call verbatim to the user in markdown. Then write AGENT SUMMARY: and then include a summary of what you did."
    agent_name = AgentType.KNOWLEDGE.value

    @staticmethod
    @kernel_function(description="Search the AI Search knowledge base for the given query")
    async def search_knowledge_base(
        query: str, 
        top: int = 3,
        filter: Optional[str] = None
    ) -> str:
        """Search the AI Search knowledge base for the given query.

        Args:
            query: The search query text
            top: Maximum number of results to return
            filter: Optional filter expression

        Returns:
            JSON string containing the search results
        """
        try:
            # Get the search client
            search_client = config.get_search_client()
            if not search_client:
                return json.dumps({
                    "success": False,
                    "error": "Azure AI Search is not enabled or configured. Please check your configuration.",
                    "results": []
                })

            # Execute the search
            results = search_client.search(
                search_text=query,
                top=top,
                select=["id", "content", "title", "url", "filepath"],
                filter=filter
            )

            # Format results
            formatted_results = []
            for result in results:
                formatted_result = {
                    "id": result["id"] if "id" in result else None,
                    "title": result["title"] if "title" in result else None,
                    "content": result["content"] if "content" in result else None,
                    "url": result["url"] if "url" in result else None,
                    "filepath": result["filepath"] if "filepath" in result else None,
                    "score": result["@search.score"] if "@search.score" in result else None
                }
                formatted_results.append(formatted_result)

            return json.dumps({
                "success": True,
                "query": query,
                "results": formatted_results
            }, indent=2) + f"\n\n{KnowledgeTools.formatting_instructions}"

        except HttpResponseError as e:
            logging.error(f"Error searching AI Search: {e}")
            return json.dumps({
                "success": False,
                "error": str(e),
                "results": []
            })
        except Exception as e:
            logging.error(f"Error during knowledge search: {e}")
            return json.dumps({
                "success": False,
                "error": str(e),
                "results": []
            })

    @staticmethod
    @kernel_function(description="Search for files containing the query text")
    async def file_search(
        query: str,
        file_types: str = "txt,md",
        max_results: int = 5
    ) -> str:
        """Search for files containing the query text.
        
        Args:
            query: Text to search for
            file_types: Comma-separated file extensions to include
            max_results: Maximum number of results to return
            
        Returns:
            JSON string containing matching file paths and content snippets
        """
        if not config.FILE_SEARCH_ENABLED:
            return json.dumps({
                "success": False,
                "error": "File search is not enabled",
                "results": []
            })
            
        search_path = config.FILE_SEARCH_PATH
        if not search_path or not os.path.exists(search_path):
            return json.dumps({
                "success": False,
                "error": f"File search path not configured or doesn't exist: {search_path}",
                "results": []
            })
            
        try:
            # Parse file types to include
            extensions = [f".{ext.strip()}" for ext in file_types.split(",")]
            
            results = []
            for root, _, files in os.walk(search_path):
                for file in files:
                    # Check if file extension matches requested types
                    if not any(file.endswith(ext) for ext in extensions):
                        continue
                        
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Check if the query appears in the content
                        if query.lower() in content.lower():
                            # Find the context of the match (snippet)
                            lower_content = content.lower()
                            match_idx = lower_content.find(query.lower())
                            start_idx = max(0, match_idx - 100)
                            end_idx = min(len(content), match_idx + len(query) + 100)
                            
                            snippet = content[start_idx:end_idx]
                            if start_idx > 0:
                                snippet = "..." + snippet
                            if end_idx < len(content):
                                snippet = snippet + "..."
                                
                            results.append({
                                "filepath": file_path,
                                "filename": file,
                                "snippet": snippet
                            })
                            
                            if len(results) >= max_results:
                                break
                    except Exception as e:
                        logging.warning(f"Error reading file {file_path}: {e}")
                        
                if len(results) >= max_results:
                    break
                    
            return json.dumps({
                "success": True,
                "query": query,
                "results": results
            }, indent=2) + f"\n\n{KnowledgeTools.formatting_instructions}"
            
        except Exception as e:
            logging.error(f"Error during file search: {e}")
            return json.dumps({
                "success": False,
                "error": str(e),
                "results": []
            })

    @staticmethod
    @kernel_function(description="Get information about the configured knowledge base")
    async def get_knowledge_base_info() -> str:
        """Get information about the configured knowledge base.
        
        Returns:
            JSON string with details about the knowledge base configuration
        """
        ai_search_enabled = config.AZURE_SEARCH_ENABLED
        file_search_enabled = config.FILE_SEARCH_ENABLED
        
        info = {
            "ai_search": {
                "enabled": ai_search_enabled,
                "endpoint": config.AZURE_SEARCH_ENDPOINT if ai_search_enabled else None,
                "index_name": config.AZURE_SEARCH_INDEX_NAME if ai_search_enabled else None
            },
            "file_search": {
                "enabled": file_search_enabled,
                "search_path": config.FILE_SEARCH_PATH if file_search_enabled else None
            }
        }
        
        return json.dumps(info, indent=2) + f"\n\n{KnowledgeTools.formatting_instructions}"

    @staticmethod
    def generate_tools_json_doc() -> Dict[str, Any]:
        """Generate tools JSON documentation for the Knowledge Agent.
        
        Returns:
            Dictionary containing the tools JSON
        """
        return {
            "name": "Knowledge_Agent",
            "description": "Agent with access to knowledge bases for answering questions using AI Search or file search",
            "tools": [
                {
                    "name": "search_knowledge_base",
                    "description": "Search the AI Search knowledge base for the given query",
                    "parameters": {
                        "query": {
                            "type": "string",
                            "description": "The search query text"
                        },
                        "top": {
                            "type": "integer",
                            "description": "Maximum number of results to return"
                        },
                        "filter": {
                            "type": "string",
                            "description": "Optional filter expression"
                        }
                    }
                },
                {
                    "name": "file_search",
                    "description": "Search for files containing the query text",
                    "parameters": {
                        "query": {
                            "type": "string",
                            "description": "Text to search for"
                        },
                        "file_types": {
                            "type": "string",
                            "description": "Comma-separated file extensions to search (e.g. 'txt,md,pdf')"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of files to return"
                        }
                    }
                },
                {
                    "name": "get_knowledge_base_info",
                    "description": "Get information about the configured knowledge base",
                    "parameters": {}
                }
            ]
        }

    @staticmethod
    def get_all_kernel_functions() -> Dict[str, Any]:
        """Get all kernel functions for the Knowledge Agent.
        
        Returns:
            Dictionary mapping function names to function objects
        """
        return {
            "search_knowledge_base": KnowledgeTools.search_knowledge_base,
            "file_search": KnowledgeTools.file_search,
            "get_knowledge_base_info": KnowledgeTools.get_knowledge_base_info
        }
