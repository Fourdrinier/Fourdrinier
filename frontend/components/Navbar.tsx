import { FC } from "react";
import Image from "next/image";
import Link from "next/link";

const Navbar: FC = () => {
    return (
        <nav className="fixed top-0 left-0 right-0 w-full flex items-center justify-between p-4 bg-gray-800 text-white shadow-md z-50">
            <div className="flex items-center">
                <Link href="/" passHref>
                    <Image src="/logo.png" alt="Logo" width={40} height={40} className="mr-2" />
                </Link>
            </div>
        </nav >
    );
};

export default Navbar;