"use client"
import Navbar from '../../components/navigation/Navbar'
import Login from '../../components/auth/login'

export default function app () {
    return(
        <main className="flex min-h-screen flex-col items-center justify-between p-20">
            <Navbar currentPage={'login'} />
            <Login />
        </main>
    )
}