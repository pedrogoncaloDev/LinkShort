const STEPS = [
  {
    num: '01',
    title: 'Cole o link',
    desc: 'Jogue a URL longa na caixa da página inicial. Não precisa de conta pra começar.',
  },
  {
    num: '02',
    title: 'Personalize (se quiser)',
    desc: 'Defina uma data de expiração, ou deixe no automático.',
  },
  {
    num: '03',
    title: 'Compartilhe',
    desc: 'Copie o link curto e compartilhe onde quiser.',
  },
]

export default function HowItWorks() {
  return (
    <section className="section">
      <div className="section-head">
        <div className="section-eyebrow">Como funciona</div>
        <h2>Três passos, nenhum atrito</h2>
        <p>
          Pensado pra quem só quer colar um link e seguir em frente — sem
          telas extras no meio do caminho.
        </p>
      </div>

      <div className="steps">
        {STEPS.map((step) => (
          <div className="step" key={step.num}>
            <div className="step-num">{step.num}</div>
            <h3>{step.title}</h3>
            <p>{step.desc}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
