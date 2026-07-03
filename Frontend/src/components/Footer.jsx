import React from "react";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <div className="footer-brand">
          <span className="brand-mark">⚡</span>
          <span>TechMart Electrical</span>
        </div>

        <p>
          Wiring, lighting, switches, tools &amp; more — powering your
          projects since day one.
        </p>

        <p className="footer-copy">
          © {new Date().getFullYear()} TechMart Electrical Supplies. All rights
          reserved.
        </p>
      </div>
    </footer>
  );
}