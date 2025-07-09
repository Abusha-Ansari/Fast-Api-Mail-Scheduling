// app/api/send/route.ts
import { NextRequest, NextResponse } from "next/server";
import { Resend } from "resend";
import { EmailTemplate } from "@/templates/EmailTemplate";
import { JobOfferTemplate } from "@/templates/JobOfferTemplate";
import { EmailProps } from "@/interfaces/interfaces";
import { InterviewInviteTemplate } from '@/templates/InterviewInviteTemplate';
import { EventReminderTemplate } from '@/templates/EventReminderTemplate';
import { ThankYouTemplate } from '@/templates/ThankYouTemplate';
import { PaymentConfirmationTemplate } from '@/templates/PaymentConfirmationTemplate';
import { withRateLimit } from "@/lib/withRateLimit";


const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(req: NextRequest) {

  const rateLimitResponse = await withRateLimit(req)
  if (rateLimitResponse) return rateLimitResponse
  
  const emailData: EmailProps = await req.json();

  const { to, from, subject, bodyMessage, templateType, templateData } = emailData;

  if (!to || !from || !subject) {
    return NextResponse.json({ error: "Missing required fields" }, { status: 400 });
  }

  let reactTemplate;

  switch (templateType) {
  case "job-offer":
    if (!templateData?.company || !templateData?.position || !templateData?.description) {
      return NextResponse.json({ error: "Missing template data" }, { status: 400 });
    }
    reactTemplate = JobOfferTemplate({
      company: templateData.company,
      position: templateData.position,
      description: templateData.description,
    });
    break;

  case "interview-invite":
    if (!templateData?.company || !templateData?.position || !templateData?.date || !templateData?.time || !templateData?.location) {
      return NextResponse.json({ error: "Missing template data" }, { status: 400 });
    }
    reactTemplate = InterviewInviteTemplate({
      to,
      company: templateData.company,
      position: templateData.position,
      date: templateData.date,
      time: templateData.time,
      location: templateData.location
    });
    break;

  case "event-reminder":
    if (!templateData?.eventName || !templateData?.date || !templateData?.time || !templateData?.venue) {
      return NextResponse.json({ error: "Missing template data" }, { status: 400 });
    }
    reactTemplate = EventReminderTemplate({
      eventName: templateData.eventName,
      date: templateData.date,
      time: templateData.time,
      venue: templateData.venue,
    });
    break;

  case "thank-you":
    if (!templateData?.recipientName || !templateData?.message) {
      return NextResponse.json({ error: "Missing template data" }, { status: 400 });
    }
    reactTemplate = ThankYouTemplate({
      recipientName: templateData.recipientName,
      message: templateData.message,
    });
    break;

  case "payment-confirmation":
    if (!templateData?.recipientName || !templateData?.amount || !templateData?.transactionId || !templateData?.date) {
      return NextResponse.json({ error: "Missing template data" }, { status: 400 });
    }
    reactTemplate = PaymentConfirmationTemplate({
      recipientName: templateData.recipientName,
      amount: templateData.amount,
      transactionId: templateData.transactionId,
      date: templateData.date,
    });
    break;

  default:
    if (!bodyMessage) {
      return NextResponse.json({ error: "Missing email body" }, { status: 400 });
    }
    reactTemplate = EmailTemplate({ Body: bodyMessage });
    break;
}


  try {
    const { data, error } = await resend.emails.send({
      from: "Mail Assist <mailassist@abusha.tech>",
      to: [to],
      subject,
      react: reactTemplate,
    });

    if (error) {
      return NextResponse.json({ error }, { status: 500 });
    }

    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: "Server error"+`${error}` }, { status: 500 });
  }
}
