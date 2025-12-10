import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw, Zap } from 'lucide-react';

const MonteCarloVisualization = () => {
  const canvasRef = useRef(null);
  const [isRunning, setIsRunning] = useState(false);
  const [points, setPoints] = useState([]);
  const [insideCircle, setInsideCircle] = useState(0);
  const [totalPoints, setTotalPoints] = useState(0);
  const [piEstimate, setPiEstimate] = useState(0);
  const [speed, setSpeed] = useState(10);
  const animationRef = useRef(null);

  const CANVAS_SIZE = 400;
  const RADIUS = CANVAS_SIZE / 2;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // נקה את הקנבס
    ctx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
    
    // צייר רקע
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
    
    // צייר ריבוע
    ctx.strokeStyle = '#60a5fa';
    ctx.lineWidth = 2;
    ctx.strokeRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
    
    // צייר רבע מעגל
    ctx.beginPath();
    ctx.arc(0, 0, RADIUS * 2, 0, Math.PI / 2);
    ctx.strokeStyle = '#22d3ee';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // מלא רבע מעגל בשקיפות
    ctx.fillStyle = 'rgba(34, 211, 238, 0.1)';
    ctx.fill();
    
    // צייר נקודות
    points.forEach(point => {
      ctx.beginPath();
      ctx.arc(point.x, point.y, 2, 0, Math.PI * 2);
      ctx.fillStyle = point.inside ? '#22c55e' : '#ef4444';
      ctx.fill();
    });
    
  }, [points]);

  useEffect(() => {
    if (isRunning) {
      const addPoints = () => {
        const newPoints = [];
        let newInside = insideCircle;
        
        for (let i = 0; i < speed; i++) {
          const x = Math.random() * CANVAS_SIZE;
          const y = Math.random() * CANVAS_SIZE;
          const distance = Math.sqrt(x * x + y * y);
          const inside = distance <= RADIUS * 2;
          
          newPoints.push({ x, y, inside });
          if (inside) newInside++;
        }
        
        setPoints(prev => [...prev, ...newPoints]);
        setInsideCircle(newInside);
        setTotalPoints(prev => prev + speed);
        
        const newTotal = totalPoints + speed;
        if (newTotal > 0) {
          setPiEstimate((newInside / newTotal) * 4);
        }
        
        animationRef.current = requestAnimationFrame(addPoints);
      };
      
      animationRef.current = requestAnimationFrame(addPoints);
    } else {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    }
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isRunning, speed, insideCircle, totalPoints]);

  const reset = () => {
    setIsRunning(false);
    setPoints([]);
    setInsideCircle(0);
    setTotalPoints(0);
    setPiEstimate(0);
  };

  const addBurst = () => {
    const newPoints = [];
    let newInside = insideCircle;
    
    for (let i = 0; i < 1000; i++) {
      const x = Math.random() * CANVAS_SIZE;
      const y = Math.random() * CANVAS_SIZE;
      const distance = Math.sqrt(x * x + y * y);
      const inside = distance <= RADIUS * 2;
      
      newPoints.push({ x, y, inside });
      if (inside) newInside++;
    }
    
    setPoints(prev => [...prev, ...newPoints]);
    setInsideCircle(newInside);
    setTotalPoints(prev => prev + 1000);
    setPiEstimate((newInside / (totalPoints + 1000)) * 4);
  };

  const accuracy = totalPoints > 0 ? 
    (100 - Math.abs((piEstimate - Math.PI) / Math.PI * 100)).toFixed(2) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-8" dir="rtl">
      <div className="max-w-6xl mx-auto">
        
        {/* כותרת */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-white mb-3">
            🎰 שיטת מונטה קרלו
          </h1>
          <p className="text-xl text-blue-200">
            פתרון בעיות באמצעות אקראיות מבוקרת
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          
          {/* קנבס */}
          <div className="bg-slate-800 rounded-xl p-6 shadow-2xl">
            <h2 className="text-2xl font-bold text-white mb-4 text-center">
              🎯 הדמיה ויזואלית
            </h2>
            
            <div className="relative">
              <canvas
                ref={canvasRef}
                width={CANVAS_SIZE}
                height={CANVAS_SIZE}
                className="border-4 border-slate-700 rounded-lg"
              />
              
              {/* מקרא */}
              <div className="mt-4 flex gap-4 justify-center text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-green-500"></div>
                  <span className="text-gray-300">בתוך המעגל</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-red-500"></div>
                  <span className="text-gray-300">מחוץ למעגל</span>
                </div>
              </div>
            </div>
          </div>

          {/* פאנל בקרה וסטטיסטיקות */}
          <div className="space-y-6">
            
            {/* סטטיסטיקות */}
            <div className="bg-slate-800 rounded-xl p-6 shadow-2xl">
              <h2 className="text-2xl font-bold text-white mb-4">📊 תוצאות</h2>
              
              <div className="space-y-4">
                {/* הערכת π */}
                <div className="bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg p-4">
                  <div className="text-sm text-white/80 mb-1">הערכת π</div>
                  <div className="text-4xl font-bold text-white">
                    {piEstimate.toFixed(6)}
                  </div>
                  <div className="text-sm text-white/60 mt-1">
                    π האמיתי: 3.141593
                  </div>
                </div>

                {/* נקודות */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-slate-700 rounded-lg p-4">
                    <div className="text-sm text-gray-400 mb-1">סה"כ נקודות</div>
                    <div className="text-2xl font-bold text-white">
                      {totalPoints.toLocaleString()}
                    </div>
                  </div>
                  
                  <div className="bg-slate-700 rounded-lg p-4">
                    <div className="text-sm text-gray-400 mb-1">דיוק</div>
                    <div className="text-2xl font-bold text-green-400">
                      {accuracy}%
                    </div>
                  </div>
                </div>

                {/* פירוט נקודות */}
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="bg-green-500/20 border border-green-500/50 rounded-lg p-3">
                    <div className="text-green-300 mb-1">בתוך המעגל</div>
                    <div className="text-xl font-bold text-green-400">
                      {insideCircle.toLocaleString()}
                    </div>
                  </div>
                  
                  <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-3">
                    <div className="text-red-300 mb-1">מחוץ למעגל</div>
                    <div className="text-xl font-bold text-red-400">
                      {(totalPoints - insideCircle).toLocaleString()}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* בקרות */}
            <div className="bg-slate-800 rounded-xl p-6 shadow-2xl">
              <h2 className="text-2xl font-bold text-white mb-4">🎮 בקרות</h2>
              
              <div className="space-y-4">
                {/* כפתורים */}
                <div className="flex gap-3">
                  <button
                    onClick={() => setIsRunning(!isRunning)}
                    className={`flex-1 flex items-center justify-center gap-2 px-6 py-3 rounded-lg font-bold transition-all ${
                      isRunning
                        ? 'bg-yellow-500 hover:bg-yellow-600 text-slate-900'
                        : 'bg-green-500 hover:bg-green-600 text-white'
                    }`}
                  >
                    {isRunning ? (
                      <>
                        <Pause size={20} />
                        השהה
                      </>
                    ) : (
                      <>
                        <Play size={20} />
                        התחל
                      </>
                    )}
                  </button>
                  
                  <button
                    onClick={reset}
                    className="px-6 py-3 bg-red-500 hover:bg-red-600 text-white rounded-lg font-bold transition-all flex items-center gap-2"
                  >
                    <RotateCcw size={20} />
                    אפס
                  </button>
                </div>

                {/* הוסף התפרצות */}
                <button
                  onClick={addBurst}
                  disabled={isRunning}
                  className="w-full px-6 py-3 bg-purple-500 hover:bg-purple-600 disabled:bg-slate-600 disabled:cursor-not-allowed text-white rounded-lg font-bold transition-all flex items-center justify-center gap-2"
                >
                  <Zap size={20} />
                  הוסף 1,000 נקודות
                </button>

                {/* מהירות */}
                <div>
                  <label className="block text-sm text-gray-300 mb-2">
                    מהירות: {speed} נקודות/פריים
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="50"
                    value={speed}
                    onChange={(e) => setSpeed(parseInt(e.target.value))}
                    className="w-full"
                  />
                </div>
              </div>
            </div>

            {/* נוסחה */}
            <div className="bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/50 rounded-xl p-6">
              <h3 className="text-lg font-bold text-white mb-3">🔢 הנוסחה</h3>
              <div className="bg-slate-900/50 rounded-lg p-4 font-mono text-cyan-300 text-center text-lg">
                π ≈ 4 × (נקודות במעגל / סה"כ נקודות)
              </div>
              <p className="text-sm text-gray-300 mt-3 leading-relaxed">
                ככל שנוסיף יותר נקודות אקראיות, ההערכה שלנו ל-π תהיה מדויקת יותר!
              </p>
            </div>
          </div>
        </div>

        {/* הסבר */}
        <div className="mt-8 bg-slate-800 rounded-xl p-6 shadow-2xl">
          <h2 className="text-2xl font-bold text-white mb-4">💡 איך זה עובד?</h2>
          <div className="grid md:grid-cols-3 gap-6 text-gray-300">
            <div className="space-y-2">
              <div className="text-4xl mb-2">1️⃣</div>
              <h3 className="font-bold text-white">זריקת נקודות אקראיות</h3>
              <p className="text-sm">
                זורקים נקודות באופן אקראי לתוך ריבוע שמכיל רבע מעגל
              </p>
            </div>
            
            <div className="space-y-2">
              <div className="text-4xl mb-2">2️⃣</div>
              <h3 className="font-bold text-white">ספירה</h3>
              <p className="text-sm">
                סופרים כמה נקודות נפלו בתוך המעגל וכמה מחוצה לו
              </p>
            </div>
            
            <div className="space-y-2">
              <div className="text-4xl mb-2">3️⃣</div>
              <h3 className="font-bold text-white">חישוב π</h3>
              <p className="text-sm">
                היחס בין הנקודות במעגל לכלל הנקודות מאפשר לחשב את π
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MonteCarloVisualization;