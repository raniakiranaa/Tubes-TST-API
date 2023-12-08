"use client"
import Navbar from '../../components/navigation/Navbar'
import ChatComponent from '../../components/chatbot/Chatbot'

export default function app () {
    return(
        <main className="flex min-h-screen flex-col items-center justify-between p-20">
            <Navbar currentPage={ 'chat' }/>
            <ChatComponent />
        </main>
    )
}