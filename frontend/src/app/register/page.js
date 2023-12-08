"use client"
import Navbar from '../../components/navigation/Navbar'
import Register from '../../components/auth/register'

export default function app () {
    return(
        <main className="flex min-h-screen flex-col items-center justify-between p-20">
            <Navbar currentPage={'register'} />
            <Register />
        </main>
    )
}