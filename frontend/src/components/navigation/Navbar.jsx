import React from 'react';

const Navbar = ({ currentPage }) => {
  return (
    <nav className="p-4 shadow-sm" style = {
        {
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            position: 'fixed',
            width: '100%',
            top: '0',
            backgroundColor: '#F9FFFF',
            zIndex: '30',
        }
    }>
      <div className="pl-12 text-black bold-18">HeyBuddy</div>
      <div>
        <ul className="flex pr-12 text-black medium-16">
        {currentPage === 'chat' ? (
            <li className={`mr-4 text-indigo-500`}>
              <a href="/">Logout</a>
            </li>
          ) : (
            <>
              <li className={`mr-12 text-indigo-500 ${currentPage === 'login' ? 'font-extrabold' : ''}`}>
                <a href="/login">Login</a>
              </li>
              <li className={`mr-4 text-indigo-500 ${currentPage === 'register' ? 'font-extrabold' : ''}`}>
                <a href="/register">Sign up</a>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;

