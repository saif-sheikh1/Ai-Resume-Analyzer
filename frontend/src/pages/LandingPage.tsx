import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  FileSearch, Zap, Target, Shield, BarChart3, Sparkles,
  Upload, Brain, CheckCircle2, ArrowRight, Star, Users, TrendingUp,
  ChevronDown, FileText, MessageSquare, Award
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Navbar } from "@/components/layout/Navbar";
import { useState } from "react";

const fadeInUp = {
  initial: { opacity: 0, y: 30 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6 }
};

const staggerChildren = {
  animate: { transition: { staggerChildren: 0.1 } }
};

/* ─── Hero Section ─────────────────────────────────────────── */
function HeroSection() {
  return (
    <section className="relative min-h-[90vh] flex items-center overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-[hsl(239,84%,67%/0.15)] rounded-full blur-3xl animate-float" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-[hsl(263,70%,58%/0.1)] rounded-full blur-3xl animate-float" style={{ animationDelay: "2s" }} />
        <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-[hsl(142,71%,45%/0.08)] rounded-full blur-3xl animate-float" style={{ animationDelay: "4s" }} />
      </div>

      <div className="container mx-auto px-4 py-20 text-center">


        <motion.h1
          className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-6"
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.1 }}
        >
          Your Resume,{" "}
          <span className="gradient-text">Supercharged</span>
          <br />
          with AI Intelligence
        </motion.h1>

        <motion.p
          className="text-lg md:text-xl text-[hsl(var(--muted-foreground))] max-w-2xl mx-auto mb-10"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          Upload your resume and get instant ATS scoring, AI-powered analysis,
          job matching, cover letters, and interview preparation — all in one platform.
        </motion.p>

        <motion.div
          className="flex flex-col sm:flex-row items-center justify-center gap-4"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
          <Link to="/register">
            <Button size="lg" className="text-base px-8 gap-2 animate-pulse-glow">
              Get Started Free <ArrowRight className="h-5 w-5" />
            </Button>
          </Link>
          <a href="#features">
            <Button variant="outline" size="lg" className="text-base px-8">
              See Features
            </Button>
          </a>
        </motion.div>
      </div>
    </section>
  );
}

/* ─── Features Section ─────────────────────────────────────── */
const features = [
  { icon: BarChart3, title: "ATS Score Analysis", desc: "Get a detailed ATS compatibility score with section-by-section breakdown and actionable insights." },
  { icon: Brain, title: "AI Resume Analysis", desc: "Gemini AI provides strengths, weaknesses, missing skills, and improved bullet points." },
  { icon: Target, title: "Job Matching", desc: "Compare your resume against any job description to see your match percentage." },
  { icon: FileText, title: "Cover Letter Generator", desc: "Generate tailored cover letters in professional, creative, or technical tones." },
  { icon: MessageSquare, title: "Interview Preparation", desc: "Get HR, technical, behavioral, and coding questions with sample answers." },
  { icon: Shield, title: "Secure & Private", desc: "Enterprise-grade security with encrypted storage and JWT authentication." },
];

function FeaturesSection() {
  return (
    <section id="features" className="py-24 bg-[hsl(var(--muted)/0.3)]">
      <div className="container mx-auto px-4">
        <motion.div className="text-center mb-16" {...fadeInUp} viewport={{ once: true }} whileInView="animate" initial="initial">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Everything You Need to <span className="gradient-text">Land Your Dream Job</span>
          </h2>
          <p className="text-[hsl(var(--muted-foreground))] text-lg max-w-2xl mx-auto">
            A comprehensive suite of AI-powered tools designed to optimize your job search.
          </p>
        </motion.div>

        <motion.div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6" variants={staggerChildren} initial="initial" whileInView="animate" viewport={{ once: true }}>
          {features.map((feature, i) => (
            <motion.div key={i} variants={fadeInUp}>
              <Card className="h-full group hover:border-[hsl(var(--primary)/0.5)] transition-all duration-300 hover:-translate-y-1">
                <CardContent className="p-6">
                  <div className="h-12 w-12 rounded-xl gradient-primary flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                    <feature.icon className="h-6 w-6 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                  <p className="text-sm text-[hsl(var(--muted-foreground))]">{feature.desc}</p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}

/* ─── How It Works ─────────────────────────────────────────── */
const steps = [
  { icon: Upload, title: "Upload Resume", desc: "Upload your PDF, DOC, or DOCX resume" },
  { icon: FileSearch, title: "AI Analysis", desc: "Our AI parses and analyzes every section" },
  { icon: BarChart3, title: "Get Your Score", desc: "Receive detailed ATS score and insights" },
  { icon: Zap, title: "Optimize & Apply", desc: "Apply improvements and match to jobs" },
];

function HowItWorksSection() {
  return (
    <section className="py-24">
      <div className="container mx-auto px-4">
        <motion.div className="text-center mb-16" {...fadeInUp} viewport={{ once: true }} whileInView="animate" initial="initial">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">How It Works</h2>
          <p className="text-[hsl(var(--muted-foreground))] text-lg">Four simple steps to a better resume</p>
        </motion.div>

        <div className="grid md:grid-cols-4 gap-8">
          {steps.map((step, i) => (
            <motion.div
              key={i}
              className="text-center relative"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.15 }}
              viewport={{ once: true }}
            >
              <div className="relative inline-block mb-6">
                <div className="h-16 w-16 rounded-2xl gradient-primary flex items-center justify-center mx-auto">
                  <step.icon className="h-8 w-8 text-white" />
                </div>
                <div className="absolute -top-2 -right-2 h-6 w-6 rounded-full bg-[hsl(var(--primary))] text-white text-xs flex items-center justify-center font-bold">
                  {i + 1}
                </div>
              </div>
              <h3 className="text-lg font-semibold mb-2">{step.title}</h3>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">{step.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ─── Stats Section ────────────────────────────────────────── */
const stats = [
  { icon: Users, value: "10,000+", label: "Resumes Analyzed" },
  { icon: TrendingUp, value: "95%", label: "Accuracy Rate" },
  { icon: Star, value: "4.9/5", label: "User Rating" },
  { icon: Award, value: "85%", label: "Interview Success" },
];

function StatsSection() {
  return (
    <section className="py-20 gradient-primary">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat, i) => (
            <motion.div
              key={i}
              className="text-center text-white"
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.1 }}
              viewport={{ once: true }}
            >
              <stat.icon className="h-8 w-8 mx-auto mb-3 opacity-80" />
              <div className="text-3xl md:text-4xl font-bold mb-1">{stat.value}</div>
              <div className="text-sm opacity-80">{stat.label}</div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}


/* ─── Interactive ATS Scanner Section ─────────────────────── */
function InteractiveScannerSection() {
  const [isScanning, setIsScanning] = useState(false);
  const [scanComplete, setScanComplete] = useState(false);

  const handleScan = () => {
    setIsScanning(true);
    setScanComplete(false);
    setTimeout(() => {
      setIsScanning(false);
      setScanComplete(true);
    }, 3000);
  };

  return (
    <section className="py-24 bg-[hsl(var(--muted)/0.3)] overflow-hidden">
      <div className="container mx-auto px-4">
        <motion.div className="text-center mb-16" {...fadeInUp} viewport={{ once: true }}>
          <h2 className="text-3xl md:text-4xl font-bold mb-4">See the AI in Action</h2>
          <p className="text-[hsl(var(--muted-foreground))] text-lg">Watch how our ATS simulator extracts and analyzes data instantly.</p>
        </motion.div>

        <div className="max-w-5xl mx-auto grid md:grid-cols-2 gap-12 items-center">
          {/* Mock Document */}
          <motion.div 
            className="relative glass rounded-xl p-8 border border-[hsl(var(--border))] shadow-2xl h-[400px] overflow-hidden bg-white/5 dark:bg-black/20"
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
          >
            {isScanning && (
              <div className="absolute left-0 w-full h-1 bg-[hsl(var(--primary))] shadow-[0_0_15px_hsl(var(--primary))] z-10 animate-scan" />
            )}
            <div className="space-y-4 opacity-70">
              <div className="h-6 w-1/3 bg-[hsl(var(--foreground)/0.2)] rounded" />
              <div className="h-4 w-1/4 bg-[hsl(var(--foreground)/0.15)] rounded mb-8" />
              
              <div className="space-y-2">
                <div className="h-3 w-full bg-[hsl(var(--foreground)/0.1)] rounded" />
                <div className="h-3 w-5/6 bg-[hsl(var(--foreground)/0.1)] rounded" />
                <div className="h-3 w-4/6 bg-[hsl(var(--foreground)/0.1)] rounded" />
              </div>
              
              <div className="pt-6 space-y-2">
                <div className="h-4 w-1/4 bg-[hsl(var(--foreground)/0.2)] rounded mb-2" />
                <div className="h-3 w-full bg-[hsl(var(--foreground)/0.1)] rounded" />
                <div className="h-3 w-full bg-[hsl(var(--foreground)/0.1)] rounded" />
                <div className="h-3 w-3/4 bg-[hsl(var(--foreground)/0.1)] rounded" />
              </div>
            </div>
            
            {scanComplete && (
              <motion.div 
                className="absolute inset-0 bg-[hsl(var(--primary)/0.05)] border-2 border-[hsl(var(--primary))] rounded-xl pointer-events-none"
                initial={{ opacity: 0, scale: 1.05 }}
                animate={{ opacity: 1, scale: 1 }}
              />
            )}
          </motion.div>

          {/* Controls & Results */}
          <motion.div 
            className="flex flex-col justify-center space-y-8"
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
          >
            <div>
              <h3 className="text-2xl font-bold mb-4">Deep Keyword Extraction</h3>
              <p className="text-[hsl(var(--muted-foreground))] mb-6">
                Our engine simulates exactly how enterprise Applicant Tracking Systems parse your resume, identifying missing skills instantly.
              </p>
              <Button onClick={handleScan} disabled={isScanning} size="lg" className="w-full sm:w-auto">
                {isScanning ? (
                  <><Sparkles className="mr-2 h-4 w-4 animate-spin" /> Scanning Document...</>
                ) : (
                  <><Target className="mr-2 h-4 w-4" /> Run Live ATS Scan</>
                )}
              </Button>
            </div>

            <div className="glass rounded-xl p-6 min-h-[160px]">
              {scanComplete ? (
                <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold">ATS Compatibility Score</span>
                    <span className="text-2xl font-bold text-[hsl(var(--primary))]">87%</span>
                  </div>
                  <div className="w-full bg-[hsl(var(--muted))] h-2 rounded-full overflow-hidden">
                    <motion.div 
                      className="bg-[hsl(var(--primary))] h-full"
                      initial={{ width: 0 }}
                      animate={{ width: "87%" }}
                      transition={{ duration: 1, ease: "easeOut" }}
                    />
                  </div>
                  <div className="flex gap-2 pt-2 flex-wrap">
                    <span className="px-2 py-1 bg-green-500/20 text-green-600 dark:text-green-400 text-xs rounded-full font-medium">React found</span>
                    <span className="px-2 py-1 bg-green-500/20 text-green-600 dark:text-green-400 text-xs rounded-full font-medium">Python found</span>
                    <span className="px-2 py-1 bg-red-500/20 text-red-600 dark:text-red-400 text-xs rounded-full font-medium">Missing: Docker</span>
                  </div>
                </motion.div>
              ) : (
                <div className="flex items-center justify-center h-full text-[hsl(var(--muted-foreground))] opacity-50">
                  Click 'Run Live ATS Scan' to see results
                </div>
              )}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}


/* ─── FAQ Section ──────────────────────────────────────────── */
const faqs = [
  { q: "What file formats are supported?", a: "We support PDF, DOC, and DOCX resume files up to 10MB." },
  { q: "How accurate is the ATS scoring?", a: "Our scoring algorithm evaluates 8 key categories including formatting, skills, keywords, experience, and more — achieving 95% alignment with major ATS systems." },
  { q: "Is my resume data secure?", a: "Yes. All files are encrypted and stored securely. We use JWT authentication and enterprise-grade security practices." },
  { q: "Which AI model powers the analysis?", a: "We use Google's Gemini 1.5 Flash for fast, accurate resume analysis, cover letter generation, and interview preparation." },
  { q: "Can I compare my resume to a job description?", a: "Yes! Paste any job description and get a match percentage, skills gap analysis, and specific recommendations." },
  { q: "Are the cover letters unique?", a: "Each cover letter is generated uniquely based on your resume, the job description, and the company — never templated." },
  { q: "Can I download my analysis as a PDF?", a: "Yes, you can generate and download professional PDF reports with your ATS score, analysis, and recommendations." },
  { q: "Is there a free plan?", a: "Yes! Get started with 3 free resume uploads and basic analysis. Upgrade to Pro for unlimited access." },
];

function FAQSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section className="py-24">
      <div className="container mx-auto px-4 max-w-3xl">
        <motion.div className="text-center mb-16" {...fadeInUp} viewport={{ once: true }} whileInView="animate" initial="initial">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Frequently Asked Questions</h2>
        </motion.div>

        <div className="space-y-3">
          {faqs.map((faq, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              viewport={{ once: true }}
            >
              <Card className="cursor-pointer" onClick={() => setOpenIndex(openIndex === i ? null : i)}>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <h3 className="font-medium">{faq.q}</h3>
                    <ChevronDown className={`h-5 w-5 transition-transform ${openIndex === i ? "rotate-180" : ""}`} />
                  </div>
                  {openIndex === i && (
                    <motion.p
                      className="mt-3 text-sm text-[hsl(var(--muted-foreground))]"
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                    >
                      {faq.a}
                    </motion.p>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ─── CTA Section ──────────────────────────────────────────── */
function CTASection() {
  return (
    <section className="py-24 gradient-primary relative overflow-hidden">
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-0 left-0 w-full h-full" style={{ backgroundImage: "radial-gradient(circle at 20% 50%, white 1px, transparent 1px)", backgroundSize: "40px 40px" }} />
      </div>
      <div className="container mx-auto px-4 text-center relative z-10">
        <motion.div {...fadeInUp} viewport={{ once: true }} whileInView="animate" initial="initial">
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">Ready to Transform Your Resume?</h2>
          <p className="text-white/80 text-lg mb-8 max-w-xl mx-auto">
            Join thousands of job seekers who've improved their resumes with AI-powered insights.
          </p>
          <Link to="/register">
            <Button size="lg" className="bg-white text-[hsl(var(--primary))] hover:bg-white/90 text-base px-8">
              Start Analyzing Free <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
        </motion.div>
      </div>
    </section>
  );
}

/* ─── Footer ───────────────────────────────────────────────── */
function Footer() {
  return (
    <footer className="border-t border-[hsl(var(--border))] py-12">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="h-8 w-8 rounded-lg gradient-primary flex items-center justify-center">
                <span className="text-white font-bold text-sm">AI</span>
              </div>
              <span className="font-bold text-lg">ResumeAnalyzer</span>
            </div>
            <p className="text-sm text-[hsl(var(--muted-foreground))]">
              AI-powered resume analysis platform to help you land your dream job.
            </p>
          </div>
          <div>
            <h4 className="font-semibold mb-3">Product</h4>
            <ul className="space-y-2 text-sm text-[hsl(var(--muted-foreground))]">
              <li><a href="#features" className="hover:text-[hsl(var(--foreground))] transition-colors">Features</a></li>
              <li><Link to="/register" className="hover:text-[hsl(var(--foreground))] transition-colors">Get Started</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-3">Resources</h4>
            <ul className="space-y-2 text-sm text-[hsl(var(--muted-foreground))]">
              <li><a href="#" className="hover:text-[hsl(var(--foreground))] transition-colors">Documentation</a></li>
              <li><a href="#" className="hover:text-[hsl(var(--foreground))] transition-colors">API Reference</a></li>
              <li><a href="#" className="hover:text-[hsl(var(--foreground))] transition-colors">Blog</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-3">Legal</h4>
            <ul className="space-y-2 text-sm text-[hsl(var(--muted-foreground))]">
              <li><a href="#" className="hover:text-[hsl(var(--foreground))] transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="hover:text-[hsl(var(--foreground))] transition-colors">Terms of Service</a></li>
              <li><a href="#" className="hover:text-[hsl(var(--foreground))] transition-colors">Cookie Policy</a></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-[hsl(var(--border))] mt-8 pt-8 text-center text-sm text-[hsl(var(--muted-foreground))]">
          © {new Date().getFullYear()} AI Resume Analyzer. All rights reserved.
        </div>
      </div>
    </footer>
  );
}

/* ─── Landing Page ─────────────────────────────────────────── */
export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[hsl(var(--background))]">
      <Navbar />
      <HeroSection />
      <FeaturesSection />
      <HowItWorksSection />
      <StatsSection />
      <InteractiveScannerSection />
      <FAQSection />
      <CTASection />
      <Footer />
    </div>
  );
}
