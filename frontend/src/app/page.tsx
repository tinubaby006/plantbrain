"use client";

import { useState, useRef } from "react";
import { UploadCloud, Search, MessageSquare, Send, FileText, Database, Settings, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Label } from "@/components/ui/label";

const API_BASE = "http://127.0.0.1:8000";

export default function Home() {
  const [activeTab, setActiveTab] = useState("chat");
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");

  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  const [chatMessage, setChatMessage] = useState("");
  const [chatHistory, setChatHistory] = useState<{ role: "user" | "bot"; content: string; sources?: any[] }[]>([]);
  const [isChatting, setIsChatting] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setUploadMessage("");
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (res.ok) {
        setUploadMessage("File indexed successfully!");
        setFile(null);
        if (fileInputRef.current) fileInputRef.current.value = "";
      } else {
        setUploadMessage(data.message || "Upload failed");
      }
    } catch (err) {
      setUploadMessage("Network error during upload.");
    } finally {
      setUploading(false);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    setIsSearching(true);
    try {
      const res = await fetch(`${API_BASE}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: searchQuery, top_k: 5 }),
      });
      const data = await res.json();
      if (res.ok) {
        setSearchResults(data.data.results || []);
      }
    } catch (error) {
      console.error("Search failed", error);
    } finally {
      setIsSearching(false);
    }
  };

  const handleChat = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatMessage.trim()) return;

    const userMsg = chatMessage;
    setChatHistory((prev) => [...prev, { role: "user", content: userMsg }]);
    setChatMessage("");
    setIsChatting(true);

    try {
      const res = await fetch(`${API_BASE}/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMsg, top_k: 5, model: "gemini-3.6-flash" }),
      });
      const data = await res.json();
      if (res.ok) {
        setChatHistory((prev) => [
          ...prev,
          { role: "bot", content: data.data.answer, sources: data.data.sources },
        ]);
      } else {
        setChatHistory((prev) => [...prev, { role: "bot", content: "Error: " + data.message }]);
      }
    } catch (error) {
      setChatHistory((prev) => [...prev, { role: "bot", content: "Network error occurred." }]);
    } finally {
      setIsChatting(false);
    }
  };

  return (
    <div className="flex h-screen w-full bg-background text-foreground overflow-hidden font-sans selection:bg-primary selection:text-primary-foreground dark">

      {/* Sidebar */}
      <div className="w-80 border-r border-border bg-sidebar flex flex-col p-6 z-10">
        <div className="flex items-center gap-3 mb-10">
          <div className="bg-primary/10 p-2 rounded-sm border border-primary/20">
            <Database className="w-6 h-6 text-primary" />
          </div>
          <h1 className="text-2xl font-semibold tracking-tight">PlantBrain <span className="text-primary">AI</span></h1>
        </div>

        <div className="flex-1 space-y-8">
          <div>
            <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider mb-4 flex items-center gap-2">
              <UploadCloud className="w-4 h-4" /> Knowledge Base
            </h3>

            <Card className="bg-background border-border shadow-none rounded-sm">
              <CardContent className="p-4 flex flex-col gap-4">
                <div className="grid w-full max-w-sm items-center gap-1.5">
                  <Label htmlFor="file" className="text-xs font-semibold">Upload Document</Label>
                  <Input
                    id="file"
                    type="file"
                    onChange={handleFileChange}
                    ref={fileInputRef}
                    className="cursor-pointer file:text-primary file:bg-primary/10 file:border-0 file:rounded-sm file:px-2 file:mr-2 hover:file:bg-primary/20 text-xs rounded-sm border-border bg-sidebar"
                  />
                  <p className="text-[10px] text-muted-foreground mt-1">PDF, DOCX, TXT, CSV, XLSX, Images</p>
                </div>
                <Button
                  onClick={handleUpload}
                  disabled={!file || uploading}
                  className="w-full rounded-sm hover:bg-primary/90 transition-none shadow-none"
                >
                  {uploading ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <UploadCloud className="w-4 h-4 mr-2" />}
                  {uploading ? "Indexing..." : "Upload & Index"}
                </Button>
                {uploadMessage && (
                  <p className="text-sm text-center font-medium text-primary mt-2">{uploadMessage}</p>
                )}
              </CardContent>
            </Card>
          </div>

          <div>
            <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider mb-4 flex items-center gap-2">
              <Settings className="w-4 h-4" /> System
            </h3>
            <div className="flex flex-col gap-2">
              <Badge variant="outline" className="justify-start py-1.5 px-3 border-border bg-sidebar text-foreground w-fit rounded-sm font-normal">
                Vector DB: <span className="text-primary ml-1 font-semibold">Chroma</span>
              </Badge>
              <Badge variant="outline" className="justify-start py-1.5 px-3 border-border bg-sidebar text-foreground w-fit rounded-sm font-normal">
                Model: <span className="text-primary ml-1 font-semibold">Gemini 1.5 Flash 8B</span>
              </Badge>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col relative overflow-hidden bg-background">

        <div className="flex-1 p-8 overflow-hidden flex flex-col z-10">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="flex flex-col h-full">
            <div className="flex items-center justify-between mb-8">
              <TabsList className="bg-sidebar border border-border p-1 rounded-xl shadow-none">
                <TabsTrigger value="chat" className="rounded-lg px-6 data-[state=active]:bg-primary data-[state=active]:text-primary-foreground data-[state=active]:shadow-none transition-none">
                  <MessageSquare className="w-4 h-4 mr-2" /> RAG Chat
                </TabsTrigger>
                <TabsTrigger value="search" className="rounded-lg px-6 data-[state=active]:bg-primary data-[state=active]:text-primary-foreground data-[state=active]:shadow-none transition-none">
                  <Search className="w-4 h-4 mr-2" /> Semantic Search
                </TabsTrigger>
              </TabsList>
            </div>

            {/* RAG Chat Tab */}
            <TabsContent value="chat" className="flex-1 flex flex-col m-0 overflow-hidden outline-none data-[state=active]:flex">
              <Card className="flex-1 flex flex-col bg-card shadow-none overflow-hidden rounded-2xl">
                <CardHeader className=" border-border bg-card">
                  <CardTitle className="flex items-center gap-2 text-lg">
                    <MessageSquare className="w-5 h-5 text-primary" /> Ask PlantBrain
                  </CardTitle>
                  <CardDescription>
                    Chat with your industrial documents using Retrieval-Augmented Generation.
                  </CardDescription>
                </CardHeader>

                <ScrollArea className="flex-1 p-6">
                  <div className="flex flex-col gap-6 max-w-3xl mx-auto pb-4">
                    {chatHistory.length === 0 ? (
                      <div className="flex flex-col items-center justify-center h-full text-muted-foreground mt-20">
                        <MessageSquare className="w-12 h-12 mb-4 opacity-20" />
                        <p>No messages yet. Ask a question about your indexed documents!</p>
                      </div>
                    ) : (
                      chatHistory.map((msg, i) => (
                        <div key={i} className={`flex gap-4 ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                          {msg.role === "bot" && (
                            <Avatar className="w-8 h-8 border border-border rounded-sm">
                              <AvatarFallback className="bg-sidebar text-primary text-xs rounded-sm">AI</AvatarFallback>
                            </Avatar>
                          )}
                          <div className={`flex flex-col gap-2 max-w-[80%] ${msg.role === "user" ? "items-end" : "items-start"}`}>
                            <div className={`p-4 ${msg.role === "user"
                              ? "bg-primary text-primary-foreground shadow-none rounded-2xl rounded-tr-sm"
                              : "bg-sidebar border border-border shadow-none rounded-2xl rounded-tl-sm"
                              }`}>
                              <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                            </div>

                            {msg.sources && msg.sources.length > 0 && (
                              <div className="mt-2 w-full">
                                <p className="text-xs font-semibold text-muted-foreground mb-2 ml-1 flex items-center gap-1">
                                  <FileText className="w-3 h-3" /> Sources
                                </p>
                                <div className="flex flex-wrap gap-2">
                                  {msg.sources.map((src: any, idx: number) => (
                                    <Badge key={idx} variant="secondary" className="text-[10px] py-0.5 bg-background border-border rounded-sm font-normal">
                                      {src.metadata?.source || "Document"}
                                    </Badge>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                          {msg.role === "user" && (
                            <Avatar className="w-8 h-8 border border-border rounded-sm">
                              <AvatarFallback className="bg-background text-foreground text-xs rounded-sm">U</AvatarFallback>
                            </Avatar>
                          )}
                        </div>
                      ))
                    )}
                    {isChatting && (
                      <div className="flex gap-4 justify-start">
                        <Avatar className="w-8 h-8 border border-border rounded-sm">
                          <AvatarFallback className="bg-sidebar text-primary text-xs rounded-sm"><Loader2 className="w-3 h-3 animate-spin" /></AvatarFallback>
                        </Avatar>
                        <div className="p-4 rounded-2xl rounded-tl-sm bg-sidebar border border-border flex items-center gap-2">
                          <div className="w-1.5 h-1.5 rounded-full bg-primary/60 animate-pulse"></div>
                          <div className="w-1.5 h-1.5 rounded-full bg-primary/60 animate-pulse delay-150"></div>
                          <div className="w-1.5 h-1.5 rounded-full bg-primary/60 animate-pulse delay-300"></div>
                        </div>
                      </div>
                    )}
                  </div>
                </ScrollArea>

                <div className="p-4 bg-card border-t border-border">
                  <form onSubmit={handleChat} className="flex gap-3 max-w-3xl mx-auto relative">
                    <Input
                      placeholder="Ask anything about your documents..."
                      value={chatMessage}
                      onChange={(e) => setChatMessage(e.target.value)}
                      disabled={isChatting}
                      className="bg-background border-border focus-visible:ring-primary h-12 px-4 rounded-xl shadow-none"
                    />
                    <Button
                      type="submit"
                      disabled={isChatting || !chatMessage.trim()}
                      className="h-12 w-12 rounded-xl shrink-0 bg-primary hover:bg-primary/90 shadow-none transition-none"
                      size="icon"
                    >
                      <Send className="w-5 h-5 ml-0.5" />
                    </Button>
                  </form>
                </div>
              </Card>
            </TabsContent>

            {/* Semantic Search Tab */}
            <TabsContent value="search" className="flex-1 flex flex-col m-0 overflow-hidden outline-none data-[state=active]:flex">
              <Card className="flex-1 flex flex-col border-border bg-card shadow-none overflow-hidden rounded-xl">
                <CardHeader className="border-b border-border bg-card">
                  <CardTitle className="flex items-center gap-2 text-lg">
                    <Search className="w-5 h-5 text-primary" /> Semantic Search
                  </CardTitle>
                  <CardDescription>
                    Find exact matches and semantically similar text chunks across all documents.
                  </CardDescription>
                </CardHeader>

                <div className="p-6 border-b border-border bg-background">
                  <form onSubmit={handleSearch} className="flex gap-3 max-w-2xl mx-auto">
                    <Input
                      placeholder="Search for concepts, keywords, or phrases..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="bg-sidebar border-border focus-visible:ring-primary h-12 px-4 rounded-xl shadow-none"
                    />
                    <Button
                      type="submit"
                      disabled={isSearching || !searchQuery.trim()}
                      className="h-12 px-8 rounded-xl shrink-0 shadow-none hover:bg-primary/90 transition-none"
                    >
                      {isSearching ? <Loader2 className="w-5 h-5 animate-spin" /> : <Search className="w-5 h-5 mr-2" />}
                      Search
                    </Button>
                  </form>
                </div>

                <ScrollArea className="flex-1 p-6">
                  <div className="max-w-4xl mx-auto space-y-4 pb-4">
                    {searchResults.length === 0 && !isSearching && (
                      <div className="flex flex-col items-center justify-center h-full text-muted-foreground mt-20">
                        <Search className="w-12 h-12 mb-4 opacity-20" />
                        <p>Search results will appear here.</p>
                      </div>
                    )}

                    {searchResults.map((result, idx) => (
                      <Card key={idx} className="bg-sidebar border-border hover:border-primary/50 rounded-xl shadow-none transition-none">
                        <CardHeader className="py-3 px-4 border-b border-border flex flex-row items-center justify-between">
                          <div className="flex items-center gap-2">
                            <FileText className="w-4 h-4 text-primary" />
                            <span className="text-sm font-medium">{result.document || "Unknown Document"}</span>
                          </div>
                          <Badge variant="outline" className="text-xs bg-background border-border rounded-sm font-normal">
                            Score: <span className="text-primary font-medium ml-1">{result.distance?.toFixed(4) ?? "N/A"}</span>
                          </Badge>
                        </CardHeader>
                        <CardContent className="p-4">
                          <p className="text-sm text-muted-foreground leading-relaxed">
                            {result.text}
                          </p>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </ScrollArea>
              </Card>
            </TabsContent>

          </Tabs>
        </div>
      </div>
    </div>
  );
}
